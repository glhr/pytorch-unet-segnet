from torch import nn as nn
import torch

from segnet import SegNet

from utils import logger
from plotting import display_img
import numpy as np


class FusionNet(nn.Module):
    """PyTorch module for 'AdapNet++' and 'AdapNet++ with fusion architecture' """

    def __init__(self, fusion, bottleneck, fusion_activ, segnet_models=None, num_classes=3, decoders="multi", pretrained_last_layer=False, late_dilation=1, branches=2, viz=False):
        super(FusionNet, self).__init__()

        self.fusion = False
        self.viz = viz

        fusion_module = {
            "ssma": SSMA,
            "custom": SSMACustom
        }

        if segnet_models is None:
            segnet_models = [SegNet(num_classes=num_classes) for i in range(branches)]
        else:
            branches = len(segnet_models)
        if len(segnet_models) > 1:
            self.encoder_mod1 = segnet_models[0].encoders
            # self.encoder_mod1.res_n50_enc.layer3[2].dropout = False
            self.encoder_mod2 = segnet_models[1].encoders
            # self.encoder_mod2.res_n50_enc.layer3[2].dropout = False
            # self.ssma_s1 = SSMA(24, 6)
            # self.ssma_s2 = SSMA(24, 6)
            if branches == 3:
                self.encoder_mod3 = segnet_models[2].encoders
            else:
                self.encoder_mod3 = None
            self.ssma_res = fusion_module[fusion](
                segnet_models[0].filter_config[-1],
                bottleneck=bottleneck,
                branches=branches,
                fusion_activ=fusion_activ)

            self.decoder_mod1 = segnet_models[0].decoders
            if decoders == "multi" or decoders == "late":
                self.decoder_mod2 = segnet_models[1].decoders
                if branches == 3:
                    self.decoder_mod3 = segnet_models[2].decoders
                else:
                    self.decoder_mod3 = None
                self.classifier = fusion_module[fusion](
                    segnet_models[0].filter_config[0],
                    bottleneck=bottleneck,
                    out=num_classes,
                    branches=branches,
                    late_dilation=late_dilation,
                    fusion_activ=fusion_activ)
                if fusion=="custom" and pretrained_last_layer:
                    self.classifier.final_conv = segnet_models[0].classifier
            elif decoders == "single":
                self.decoder_mod2 = None
                self.classifier = segnet_models[0].classifier

            self.fusion = decoders
        else:
            self.encoder_mod1 = segnet_models[0].encoders
            self.decoder_mod1 = segnet_models[0].decoders
            self.classifier = segnet_models[0].classifier


    def encoder_path(self, encoder, feat):
        indices = []
        unpool_sizes = []
        feats = []
        for i in range(0, 5):
            (feat, ind), size = encoder[i](feat)
            indices.append(ind)
            unpool_sizes.append(size)
            feats.append(feat)
        return feats, indices, unpool_sizes

    def decoder_path(self, decoder, feat, indices, unpool_sizes):
        for i in range(0, 5):
            feat = decoder[i](feat, indices[4 - i], unpool_sizes[4 - i])
        return feat

    def forward(self, mod):
        logger.debug(f"{mod.shape}, {mod[:,0,:,:].unsqueeze(1).shape}")

        if self.fusion:
            # logger.info("FUSING SHIT :D")
            feat_1, indices_1, unpool_sizes_1 = self.encoder_path(self.encoder_mod1, mod[:,0,:,:].unsqueeze(1))
            # print(feat_1[-1].shape)
            feat_2, indices_2, unpool_sizes_2 = self.encoder_path(self.encoder_mod2, mod[:,1,:,:].unsqueeze(1))

            last_feats = [feat_1[-1], feat_2[-1]]
            if self.encoder_mod3 is not None:
                feat_3, indices_3, unpool_sizes_3 = self.encoder_path(self.encoder_mod3, mod[:,2,:,:].unsqueeze(1))
                last_feats.append(feat_3[-1])

            if self.fusion in ["multi","single"]:
            #m2_x, m2_s2, m2_s1 = self.encoder_mod2(mod2)
            #skip2 = self.ssma_s2(skip2, m2_s2)
            #skip1 = self.ssma_s1(skip1, m2_s1)
                feat = self.ssma_res(last_feats)
            elif self.fusion == "late":
                feat = last_feats
                if self.viz:
                    display_img(feat[0][::,-1].squeeze().detach().cpu().numpy())
        else:
            feat_1, indices_1, unpool_sizes_1 = self.encoder_path(self.encoder_mod1, mod)
            feat = feat_1[-1]

        # logger.info(self.pooling_fusion)

        if self.fusion:
            if self.fusion == "late":
                feat1 = self.decoder_path(self.decoder_mod1, feat[0], indices_1, unpool_sizes_1)
                if self.decoder_mod2 is not None:
                    feat2 = self.decoder_path(self.decoder_mod2, feat[1], indices_2, unpool_sizes_2)
                    feats = [feat1,feat2]
                    if self.decoder_mod3 is not None:
                        feat3 = self.decoder_path(self.decoder_mod3, feat[2], indices_3, unpool_sizes_3)
                        feats.append(feat3)
                    out = self.classifier(feats)
                else:
                    out = self.classifier(feat1)
                # print(out.shape)
            elif self.fusion in ["multi","single"]:
                feat1 = self.decoder_path(self.decoder_mod1, feat, indices_1, unpool_sizes_1)
                if self.decoder_mod2 is not None:
                    feat2 = self.decoder_path(self.decoder_mod2, feat, indices_2, unpool_sizes_2)
                    feats = [feat1,feat2]
                    if self.decoder_mod3 is not None:
                        feat3 = self.decoder_path(self.decoder_mod3, feat, indices_3, unpool_sizes_3)
                        feats.append(feat3)
                    out = self.classifier(feats)
                else:
                    out = self.classifier(feat1)
            # print(out.shape)
            return out
        else:
            # decoder path, upsampling with corresponding indices and size
            feat = self.decoder_path(self.decoder, feat, indices_1, unpool_sizes_1)
            return self.classifier(feat)

        #aux1, aux2, res = self.decoder(m1_x, skip1, skip2)
        #return aux1, aux2, res

class SSMA(nn.Module):

    def __init__(self, features, bottleneck, out=None, late_dilation=1, fusion_activ="sigmoid", branches=2):
        """Constructor
        :param features: number of feature maps
        :param bottleneck: bottleneck compression rate
        """
        super(SSMA, self).__init__()

        reduce_size = int(features / bottleneck)
        if out is None:
            self.final = False
            out = features
            dilation = 1
        else:
            self.final = True
            dilation = late_dilation
        double_features = int(branches * features)
        self.link = nn.Sequential(
            nn.Conv2d(double_features, reduce_size, kernel_size=3, stride=1, padding=dilation, dilation=dilation),
            nn.ReLU(),
            nn.Conv2d(reduce_size, double_features, kernel_size=3, stride=1, padding=dilation, dilation=dilation),
            nn.Sigmoid()
        )
        self.final_conv = nn.Sequential(
            nn.Conv2d(double_features, out, kernel_size=3, stride=1, padding=1),
        )

        if not self.final:
            self.bn = nn.BatchNorm2d(features)
            nn.init.kaiming_normal_(self.final_conv[0].weight, nonlinearity="relu")
        else:
            nn.init.xavier_uniform_(self.final_conv[0].weight)

        nn.init.kaiming_normal_(self.link[0].weight, nonlinearity="relu")
        nn.init.xavier_uniform_(self.link[2].weight)


    def forward(self, x_lst):
        x_12 = torch.cat(x_lst, dim=1)

        x_12_est = self.link(x_12)
        x_12 = x_12 * x_12_est
        x_12 = self.final_conv(x_12)

        # if not self.final:
        #     x_12 = self.bn(x_12)

        return x_12

class SSMACustom(nn.Module):
    def __init__(self, features, bottleneck, out=None, late_dilation=1, fusion_activ="softmax", branches=2):
        super(SSMACustom, self).__init__()

        reduce_size = int(features / bottleneck)
        if out is None:
            self.final = False
            dilation = 1
        else:
            self.final = True
            dilation = late_dilation
        double_features = int(branches * features)
        self.link = nn.Sequential(
            nn.Conv2d(double_features, reduce_size, kernel_size=3, stride=1, padding=dilation, dilation=dilation),
            nn.ReLU(),
            nn.Conv2d(reduce_size, double_features, kernel_size=3, stride=1, padding=dilation, dilation=dilation),
        )
        self.sm = nn.Softmax(dim=1) if fusion_activ == "softmax" else nn.Sigmoid()

        if self.final:
            self.final_conv = nn.Sequential(
                nn.Conv2d(features, out, kernel_size=3, stride=1, padding=1)
            )
            nn.init.xavier_uniform_(self.final_conv[0].weight)
        else:
            self.final_conv = None

        nn.init.kaiming_normal_(self.link[0].weight, nonlinearity="relu")
        nn.init.xavier_uniform_(self.link[2].weight)

        self.branches = branches


    def forward(self, m_lst):
        i_12 = torch.cat(m_lst, dim=1)
        #print(i1.shape,i2.shape, i_12.shape)

        i_12_w = self.link(i_12)
        b,c,h,w = i_12_w.shape
        i_12_w = i_12_w.view(b,self.branches,int(c/self.branches),h,w)
        #print(i_12_w.shape)
        i_12_w = self.sm(i_12_w)
        #print(i_12_w.shape)

        #x_12 = torch.sum(i_12_w, dim=1)
        x_12 = torch.unbind(i_12_w, dim=1)

        #print(i1.shape, x_12[0].shape)
        #print(i1.long()[0][0][0][:5], i2.long()[0][0][0][:5])
        fused = m_lst[0] * x_12[0]
        for f in range(1,self.branches):
            fused += (m_lst[f] * x_12[f])
        #print(fused.long()[0][0][0][:5])
        if self.final:
            fused = self.final_conv(fused)

        return fused

if __name__ == "__main__":
    segnet = SegNet(num_classes=3)
    encoder = segnet.encoders
    #print(encoder)
    fusion = FusionNet( encoders=[encoder], decoder=segnet.decoders, classifier=segnet.classifier)
    print(fusion)
    print(SSMA(features=512, bottleneck=3))
