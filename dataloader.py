import os
import numpy as np
import random
import json
import glob

import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

import cv2
from PIL import Image, ImageFile
import imageio

import albumentations as A

from utils import RANDOM_SEED, logger
from plotting import visualize_data_aug

torch.manual_seed(RANDOM_SEED)
torch.cuda.manual_seed_all(RANDOM_SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

ImageFile.LOAD_TRUNCATED_IMAGES = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class MMDataLoader(Dataset):
    def __init__(self, modalities, name, mode, augment, resize, transform=None, viz=False):
        self.idx = 0
        self.name = name
        self.idx_to_color, self.color_to_idx, self.class_to_idx, self.idx_to_idx = {}, {}, {}, {}
        self.idx_to_obj = {}

        self.modalities = modalities.copy()
        if "depthraw" in modalities:
            self.depth_completion = False
            self.modalities[self.modalities.index('depthraw')] = 'depth'
        else:
            self.depth_completion = True

        logger.warning(f"dataset modalities {self.modalities}, depth completion {self.depth_completion}")

        self.idx_to_color['objects'] = self.idx_to_color.get('objects', dict())
        self.class_to_idx['objects'] = self.class_to_idx.get('objects', dict())
        self.color_to_idx['objects'] = self.color_to_idx.get('objects', dict())
        self.idx_to_obj['objects'] = self.idx_to_obj.get('objects', dict())

        self.filenames = []

        self.augment = augment
        self.img_transforms = transforms.Compose([transforms.ToTensor()])

        self.mode = mode
        self.has_affordance_labels = False

        self.cls_labels = ["void", "impossible","possible","preferable"]

        self.aff_idx = {
            "void": -1,
            "impossible": 0,
            "possible": 1,
            "preferable": 2
        }

        self.fda_refs = glob.glob('../../datasets/fda/Rob10 scenes/*.jpg')
        self.resize = resize

        self.transform = transform
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.viz = viz

    def read_img(self, path, grayscale=True):
        return np.array(Image.open(path).convert('L'))

    def prepare_GT(self, imgGT, color_GT=False):

        if color_GT:
            #modGT = imgGT[:, :, ::-1]
            modGT = self.mask_to_class_rgb(imgGT)
        # print(modGT.shape)
        else:
            modGT = torch.tensor(imgGT, dtype=torch.long)
            if len(self.idx_to_obj):
                modGT = self.labels_to_obj(modGT)

        if self.mode == "affordances" and not self.has_affordance_labels: modGT = self.labels_obj_to_aff(modGT)

        return modGT

    def prepare_data(self, pilRGB, pilDep, pilIR, imgGT, augment, color_GT=True, save=False):

        imgGT_orig = np.array(imgGT)

        use = {
            "rgb": "rgb" in self.modalities and pilRGB is not None,
            "depth": "depth" in self.modalities and pilDep is not None,
            "ir": "ir" in self.modalities and pilIR is not None
        }

        if use["rgb"]: imgRGB_orig = np.array(pilRGB)
        #logger.debug(f"RGB range {np.min(imgRGB_orig)} {np.max(imgRGB_orig)}")
        if use["depth"]: imgDep_orig = np.array(pilDep)
        if use["ir"]: imgIR_orig = np.array(pilIR)

        img_dict = {
            'image': imgRGB_orig if use["rgb"] else None,
            'depth': imgDep_orig if use["depth"] else None,
            'ir': imgIR_orig if use["ir"] else None,
            'mask': imgGT_orig
            }

        if augment: transformed_imgs = self.data_augmentation(img_dict, apply='all')
        else: transformed_imgs = self.data_augmentation(img_dict, apply='resize_only')
        modGT = transformed_imgs['mask']
        if use["rgb"]:
            modRGB = transformed_imgs['image']
        if use["depth"]:
            modDepth = transformed_imgs['depth']
        if use["ir"]:
            modIR = transformed_imgs['ir']

        modGT = self.prepare_GT(modGT, color_GT)

        if use["rgb"]:
            if len(modRGB.shape) == 3: modRGB = modRGB[:,:,2]
            # logger.debug(f"RGB range {np.min(modRGB)} {np.max(modRGB)}")
        if use["depth"]:
            if len(modDepth.shape) == 3: modDepth = modDepth[:,:,2]
            # logger.debug(f"D range {np.min(modDepth)} {np.max(modDepth)}")
        if use["ir"]:
            if len(modIR.shape) == 3: modIR = modIR[:,:,2]
            # logger.debug(f"IR range {np.min(modIR)} {np.max(modIR)}")

        if save:
            orig_imgs = self.data_augmentation(img_dict, apply='resize_only')
            imgRGB_orig, imgGT_orig = orig_imgs['image'], orig_imgs['mask']
            imgRGB_orig = imgRGB_orig[: , :, 2]
            imgGT_orig = self.prepare_GT(imgGT_orig, color_GT)
            # print(np.unique(modGT))
            self.result_to_image(gt=modGT, orig=modRGB, folder=f"results/data_aug/{self.name}", filename_prefix=f"{self.name}-tf")
            self.result_to_image(gt=imgGT_orig, orig=imgRGB_orig, folder=f"results/data_aug/{self.name}", filename_prefix=f"{self.name}-orig")

        imgs = []
        img = {
            'rgb': modRGB if use["rgb"] else None,
            'depth': modDepth if use["depth"] else None,
            'ir': modIR if use["ir"] else None
        }
        for mod in self.modalities:
            if use[mod] and img.get(mod) is not None:
                imgs.append(torch.from_numpy(img[mod].copy()).float())

        # logger.debug(torch.unique(modGT))

        return [torch.stack(imgs), modGT]

    def remap_classes(self, idx_to_color):

        undriveable = ['sky','vegetation','obstacle','person','car','pole','tree','building','guardrail','rider','motorcycle','bicycle',
        'bus','truck','trafficlight','trafficsign','wall','fence','train','trailer','caravan','polegroup','dynamic','licenseplate','static','bridge','tunnel','car','truck','minibus','bus','cat','dog','human','building','boat','pedestrian','_background_','fence','vegetation']
        void = ['void','egovehicle','outofroi','rectificationborder','unlabeled','_ignore_']
        driveable = ['road','path','ground','lanemarking','curb']
        between = ['grass','terrain','sidewalk','parking','railtrack','ground_sidewalk']
        objclass_to_driveidx = dict()

        idx_mappings = {
            self.aff_idx["void"]: set(),
            self.aff_idx["impossible"]: set(),
            self.aff_idx["possible"]: set(),
            self.aff_idx["preferable"]: set()
        }

        for i in undriveable:
            objclass_to_driveidx[i] = self.aff_idx["impossible"]
        for i in driveable:
            objclass_to_driveidx[i] = self.aff_idx["preferable"]
        for i in between:
            objclass_to_driveidx[i] = self.aff_idx["possible"]
        for i in void:
            objclass_to_driveidx[i] = self.aff_idx["void"]


        # print(objclass_to_driveidx)
        idx_to_color_new = {
            self.aff_idx["void"]: (0,0,0),
            self.aff_idx["impossible"]: (255,0,0),
            self.aff_idx["possible"]: (255,255,0),
            self.aff_idx["preferable"]: (0,255,0)
        }
        color_to_idx_new = dict()
        conversion = dict()
        idx_to_idx = dict()
        for cls,new_idx in objclass_to_driveidx.items():
            try:
                old_idx = self.class_to_idx["objects"][cls]
                # print(old_idx)
                for v,k in idx_to_color.items():
                    # print(cls,k,v,old_idx,v==old_idx,new_idx)
                    if v==old_idx:
                        color_to_idx_new[k] = new_idx
                        conversion[old_idx] = idx_to_color_new[new_idx]
                        idx_to_idx[old_idx] = new_idx
                        if old_idx >= 0: idx_mappings[new_idx].add(old_idx)
            except KeyError:
                # print(cls, new_idx)
                pass

        idx_mappings = {k:list(v) for k,v in idx_mappings.items()}
        # print(idx_mappings)
        # print(conversion)
        # print("idx_to_idx", idx_to_idx)
        return color_to_idx_new, idx_to_color_new, conversion, idx_to_idx, idx_mappings

    def get_color(self, x, mode="objects"):
        try:
            if mode in ["affordances","convert"]:
                return self.idx_to_color["affordances"][x]
            else:
                return self.idx_to_color[mode][x]
        except KeyError:
            logger.warning(f"mapping {x} to black, idx_to_color: {self.idx_to_color}")
            return (0,0,255)

    def labels_to_color(self, labels, mode="objects"):
        bs = labels.shape
        # print(bs)
        data = np.zeros((bs[0], bs[1], 3), dtype=np.uint8)

        for idx in np.unique(labels):
            data[labels==idx] = self.get_color(idx, mode=mode)
            # print(idx, "->", self.get_color(idx, mode=mode))
        return data

    def labels_to_obj(self, gt):
        #print(torch.unique(gt))
        for orig,new in self.idx_to_obj["objects"].items():
            #print(orig,new)
            gt[gt==orig] = new
        #print(torch.unique(gt))
        return gt

    def labels_obj_to_aff(self, labels, num_cls=3, proba=False):
        if proba:
            # labels = labels.squeeze()
            # print(labels.shape)
            s = labels.shape
            new_proba = torch.zeros((labels.shape[0], num_cls, s[2], s[3])).to(self.device)
            # print(new_proba.shape)
            # print(new_proba[3])
            for idx in self.idx_mappings.keys():
                indices = [i for i in self.idx_mappings[idx] if i < labels.shape[1]]
                # print(indices)
                select = torch.index_select(labels,dim=1,index=torch.LongTensor(indices).to(self.device))
                # print(select.shape)
                s = torch.sum(select,dim=1,keepdim=True)
                # print(s.shape)
                new_proba[:,idx] = s.squeeze(1)
            # print(new_proba.shape)
            return new_proba
        else:
            new_labels = torch.zeros_like(labels)

            for old_idx in torch.unique(labels):
                new_labels[labels==old_idx] = self.idx_to_idx["convert"][old_idx.item()]
                # print(old_idx,"->",self.idx_to_idx["convert"][old_idx.item()])
            return new_labels

    def mask_to_class_rgb(self, mask, mode="objects"):
        # print('----mask->rgb----')
        mask = torch.from_numpy(np.array(mask))
        # mask = torch.squeeze(mask)  # remove 1

        # check the present values in the mask, 0 and 255 in my case
        # print('unique values rgb    ', torch.unique(mask))
        # -> unique values rgb     tensor([  0, 255], dtype=torch.uint8)

        class_mask = mask
        class_mask = class_mask.permute(2, 0, 1).contiguous()
        # print('unique values rgb    ', torch.unique(class_mask))
        h, w = class_mask.shape[1], class_mask.shape[2]
        # print(h,w)
        mask_out = torch.zeros(h, w, dtype=torch.long)

        for k in self.color_to_idx[mode]:
            # print(k)
            # print(torch.unique(class_mask), torch.tensor(k, dtype=torch.uint8).unsqueeze(1).unsqueeze(2))
            idx = (class_mask == torch.tensor(k, dtype=torch.uint8).unsqueeze(1).unsqueeze(2))
            # print(idx)
            validx = (idx.sum(0) == 3)
            # print(validx[0])

            mask_out[validx] = torch.tensor(self.color_to_idx[mode][k], dtype=torch.long)

            #print(mask_out[validx])

        # check the present values after mapping, in my case 0, 1, 2, 3
        # print('unique values mapped ', torch.unique(mask_out))
        # -> unique values mapped  tensor([0, 1, 2, 3])

        return mask_out

    def result_to_image(self, iter=None, pred_cls=None, orig=None, gt=None, pred_proba=None, proba_lst=[], folder=None, filename_prefix=None, dataset_name=None, modalities=None):
        if filename_prefix is None:
            filename_prefix = self.name

        # print(bs,np.max(b))
        concat = []

        if iter is None:
            iter = self.idx

        if orig is not None:
            if torch.is_tensor(orig):
                orig = orig.detach().cpu().numpy()
            n_modalities = len(orig)
            for m,modality in enumerate(orig):
                # print("orig shape",modality.shape)
                if np.max(modality) <= 1: modality = (modality*255)
                modality = modality.astype(np.uint8)
                if modality.shape[-1] != 3:
                    modality = np.stack((modality,)*3, axis=-1)
                    # print(np.min(orig),np.max(orig))
                    concat = concat + [modality]

                    folder = "" if folder is None else folder
                    dataset_name = self.name if dataset_name is None else dataset_name
                    # mod_i =  if n_modalities > 1 else ''
                    mod_i = '' if modalities is None else f'{modalities[m]}'
                    # if mod_i == "depth":
                    #     modality = 255 - cv2.applyColorMap(
                    #         np.uint8(modality / np.amax(modality) * 255),
                    #         cv2.COLORMAP_JET)
                    img = Image.fromarray(modality, 'RGB')
                    img.save(f'{folder}/{dataset_name}{str(iter + 1)}-{filename_prefix}{mod_i}_{self.mode}.png')

        if gt is not None:
            if torch.is_tensor(gt): gt_numpy = gt.detach().cpu().numpy()
            #concat.append(self.labels_to_color(gt_numpy, mode="objects"))
            #gt = self.labels_to_color(self.labels_obj_to_aff(gt), mode=self.mode)
            gt = self.labels_to_color(gt_numpy, mode=self.mode)
            concat.append(gt)
            # concat.append(np.stack((gt,)*3, axis=-1))

        if pred_cls is not None:
            if torch.is_tensor(pred_cls): pred_cls = pred_cls.detach().cpu().numpy()
            data = self.labels_to_color(pred_cls, mode=self.mode)
            concat.append(data)

        for cls,prob_map in enumerate(proba_lst):
            if torch.is_tensor(prob_map): prob_map = prob_map.detach().cpu().numpy()
            # print(np.unique(proba))
            # proba = pred_proba/2
            proba = (prob_map*255).astype(np.uint8)
            if cls < len(proba_lst) - 1:
                proba = np.hstack([proba, np.ones_like(proba)[:,:100]*255])
            proba = np.stack((proba,)*3, axis=-1)
            concat.append(proba)


        if pred_proba is not None:
            if torch.is_tensor(pred_proba): pred_proba = pred_proba.detach().cpu().numpy()
            # print(np.unique(proba))
            proba = pred_proba/2
            proba = (proba*255).astype(np.uint8)
            proba = np.stack((proba,)*3, axis=-1)
            concat.append(proba)

        # for d in concat:
        #     print(d.shape)
        data = np.concatenate(concat, axis=1)

        img = Image.fromarray(data, 'RGB')
        folder = "" if folder is None else folder
        dataset_name = self.name if dataset_name is None else dataset_name
        if orig is None:
            img.save(f'{folder}/{dataset_name}{str(iter + 1)}-{filename_prefix}_{self.mode}.png')

    def load_depth(self, path, invert=False):
        depth_image = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
        logger.debug(f"load_depth {np.min(depth_image)} - {np.max(depth_image)} ({type(depth_image[0][0])})")
        if isinstance(depth_image[0][0], np.uint16):
            depth_image_8u = cv2.convertScaleAbs(depth_image, alpha=(255.0/65535.0))
        else:
            depth_image_8u = depth_image

        logger.debug(f"load_depth {np.min(depth_image_8u)} - {np.max(depth_image_8u)} ({type(depth_image_8u[0][0])})")
        depth_image_8u = depth_image_8u - np.min(depth_image_8u)
        logger.debug(f"load_depth {np.min(depth_image_8u)} - {np.max(depth_image_8u)} ({type(depth_image_8u[0][0])})")
        depth_image_8u = (255 * (depth_image_8u / np.max(depth_image_8u))).astype(np.uint8)
        logger.debug(f"load_depth {np.min(depth_image_8u)} - {np.max(depth_image_8u)} ({type(depth_image_8u[0][0])})")
        if invert:
            depth_image_8u = 255 - depth_image_8u
        # if np.max(depth_image_8u) <= 1:
        #     depth_image_8u = depth_image_8u*100
        return depth_image_8u

    def data_augmentation(self, imgs, gt=None, p=0.5, save=True, apply='all'):
        # print(imgs)
        if imgs["image"] is None:
            img_height, img_width = imgs[self.modalities[0]].shape[:2]
            imgs["image"] = np.zeros_like(imgs[self.modalities[0]])
            imgs["image"] = np.dstack([imgs["image"]] * 3)
        else:
            img_height, img_width = imgs["image"].shape[:2]
        rand_crop = np.random.uniform(low=0.8, high=0.9)

        additional_targets = dict()
        for modality in ["depth", "ir"]:
            if imgs.get(modality) is not None:
                additional_targets[modality] = 'image'

        resize_transform = A.Compose([
            A.Resize(height = self.resize[1], width = self.resize[0], p=1)
            ], p=1, additional_targets=additional_targets)
        gray_transform = A.Compose([
            A.ToGray(p=1)
            ], p=1)
        color_transform = A.Compose([
            A.RandomToneCurve(scale=0.1, p=p),
            A.RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.4, brightness_by_max=False, p=p)
            ], p=1, additional_targets=additional_targets)
        geom_transform = A.Compose([
            A.GridDistortion(num_steps=3, p=p),
            A.Perspective(scale=(0.05, 0.15), pad_mode=cv2.BORDER_CONSTANT, p=p),
            A.Rotate(limit=10, p=p),
            A.RandomCrop(width=int(self.resize[0]*rand_crop), height=int(self.resize[1]*rand_crop), p=p),
            A.HorizontalFlip(p=p)
            ], p=1, additional_targets=additional_targets)

        if apply == 'resize_only':
            transformed_resized = resize_transform(image=imgs['image'], mask=imgs['mask'], depth=imgs["depth"], ir=imgs["ir"])
            transformed_gray = gray_transform(image=transformed_resized['image'], mask=transformed_resized['mask'])
            if "depth" in imgs: transformed_gray["depth"] = transformed_resized["depth"]
            if "ir" in imgs: transformed_gray["ir"] = transformed_resized["ir"]
            transformed_final = transformed_gray

        elif apply == 'all':
            transformed_resized = resize_transform(image=imgs['image'], mask=imgs['mask'], depth=imgs["depth"], ir=imgs["ir"])
            transformed_color = color_transform(image=transformed_resized['image'], mask=transformed_resized['mask'], ir=transformed_resized["ir"])
            transformed_geom = geom_transform(image=transformed_color['image'], mask=transformed_color['mask'], depth=transformed_resized["depth"], ir=transformed_color["ir"])
            transformed_gray = gray_transform(image=transformed_geom['image'], mask=transformed_geom['mask'])
            if "depth" in imgs: transformed_gray["depth"] = transformed_geom["depth"]
            if "ir" in imgs: transformed_gray["ir"] = transformed_geom["ir"]
            transformed_final = resize_transform(image=transformed_gray['image'], mask=transformed_gray['mask'], depth=transformed_gray["depth"], ir=transformed_gray["ir"])

        # print(imgs["image"].shape, transformed_gray["image"].shape)
        # print(np.unique(imgs['mask']))
        if self.viz:
            visualize_data_aug(imgs=imgs, augmented=transformed_final)

        return transformed_final

    def sample(self, sample_id, augment):
        try:
            pilRGB, pilDep, pilIR, imgGT = self.get_image_pairs(sample_id)

            return self.prepare_data(pilRGB, pilDep, pilIR, imgGT, color_GT=self.color_GT, augment=augment)
        except IOError as e:
            print("Error loading " + self.filenames[sample_id], e)
        return False, False, False

    def __len__(self):
        # print(len(self.filenames))
        return len(self.filenames)

    def __getitem__(self, idx):
        # print(self.sample(idx))
        self.idx = idx
        if self.augment:
            s = self.sample(idx, augment=True)
        else:
            s = self.sample(idx, augment=False)

        if self.transform:
            s[0] = self.transform(s[0])
        return s


class FreiburgDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/freiburg-forest/freiburg_forest_multispectral_annotated/freiburg_forest_annotated/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        """
        Initializes the data loader
        :param path: the path to the data
        """
        super().__init__(modalities, resize=resize, name="freiburg", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        if self.mode == "objects":
            self.cls_labels = [0]*len(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[4]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[4]
            self.class_to_idx['objects'][x[0].lower()] = x[4]
            if self.mode == "objects":
                self.cls_labels[x[4]] = x[0].lower()

        logger.debug(f"{self.name} - class to idx: {self.class_to_idx['objects']}")
        logger.debug(f"{self.name} - color to idx: {self.color_to_idx['objects'].values()}")

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        if set == "train":
            self.path = path + 'train/'
        elif set in ["val", "test"]:
            self.path = path + 'test/'
        elif set == "full":
            self.path = path + '**/'

        self.augment = augment
        self.viz = viz

        self.base_folders = []

        for filepath in glob.glob(self.path + 'GT_color/*.png'):
            img = filepath.split("/")[-1].split("_")[0]
            # print(img)
            self.filenames.append(img)
            self.base_folders.append(path + filepath.split("/")[-3])
        print(self.filenames[0], self.base_folders[0])

        self.suffixes = {
            'depth': "_Clipped_redict_depth_gray.png",
            "rgb": "_Clipped.jpg",
            "gt": "_mask.png",
            "ir": ".tif"
        }
        self.color_GT = True

    def get_image_pairs(self, sample_id):
        pilRGB = Image.open(self.base_folders[sample_id] + "/rgb/" + self.filenames[sample_id] + self.suffixes['rgb']).convert('RGB')
        pilDep = self.load_depth(self.base_folders[sample_id] + "/depth_gray/" + self.filenames[sample_id] + self.suffixes['depth'])
        pilIR = Image.open(self.base_folders[sample_id] + "/nir_gray/" + self.filenames[sample_id] + self.suffixes['ir']).convert('L')

        # print(self.path + "GT_color/" + a + suffixes['gt'])
        try:
            self.suffixes['gt'] = "_Clipped.png"
            # imgGT = cv2.imread(self.path + "GT_color/" + a + suffixes['gt'], cv2.IMREAD_UNCHANGED).astype(np.int8)
            imgGT = Image.open(self.base_folders[sample_id] + "/GT_color/" + self.filenames[sample_id] + self.suffixes['gt']).convert('RGB')
        except (AttributeError,IOError):
            self.suffixes['gt'] = "_mask.png"
            # imgGT = cv2.imread(self.path + "GT_color/" + a + suffixes['gt'], cv2.IMREAD_UNCHANGED).astype(np.int8)
            imgGT = Image.open(self.base_folders[sample_id] + "/GT_color/" + self.filenames[sample_id] + self.suffixes['gt']).convert('RGB')

        return pilRGB, pilDep, pilIR, imgGT


class FreiburgThermalDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/freiburg-thermal/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        """
        Initializes the data loader
        :param path: the path to the data
        """
        super().__init__(modalities, resize=resize, name="freiburgthermal", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        if self.mode == "objects":
            self.cls_labels = [0]*len(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[4]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[4]
            self.class_to_idx['objects'][x[0].lower()] = x[4]
            if self.mode == "objects":
                self.cls_labels[x[4]] = x[0].lower()

        logger.debug(f"{self.name} - class to idx: {self.class_to_idx['objects']}")
        logger.debug(f"{self.name} - color to idx: {self.color_to_idx['objects'].values()}")

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        if set in ["val", "test", "train", "full"]:
            self.path = path + 'train/'

        sequences = {
            "val": ["seq_03_day/00", "seq_03_day/01"],
            "test": ["seq_03_day/02", "seq_03_day/03", "seq_03_day/04", "seq_03_day/05"],
        }
        exclude_from_train = sum(sequences.values(), [])

        self.augment = augment
        self.viz = viz

        self.base_folders = []

        for filepath in glob.glob(self.path + 'seq_*_day/**/fl_ir_aligned/*.png'):
            img = '_'.join(filepath.split("/")[-1].split("_")[-2:])
            seq = '/'.join(filepath.split("/")[-4:-2])
            # print(seq, set)
            if (set == "full") or (set in ["val","test"] and seq in sequences[set]) or (set == "train" and seq not in exclude_from_train):
                self.filenames.append(img)
                self.base_folders.append(self.path + '/'.join(filepath.split("/")[-4:-2]))
        print(self.filenames[0], self.base_folders[0])

        self.prefixes = {
            "rgb": "fl_rgb",
            "ir": "fl_ir_aligned",
            "gt": "fl_rgb_labels"
        }
        self.color_GT = False

    def load_cropped_ir(self,path,resize=None):
        print(path)
        ir_image = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
        if resize is not None:
            ir_image = cv2.resize(ir_image, resize)
        height, width = ir_image.shape
        resize = (300, 0, width-300, height)
        ir_image = ir_image[:,300:-300]
        logger.debug(f"ir_image {np.min(ir_image)} - {np.max(ir_image)} ({type(ir_image[0][0])})")
        ir_image_8u = ir_image - np.min(ir_image)
        ir_image_8u = (255 * (ir_image_8u / np.max(ir_image_8u))).astype(np.uint8)

        return ir_image_8u

    def get_image_pairs(self, sample_id):
        pilRGB = Image.open(f"{self.base_folders[sample_id]}/{self.prefixes['rgb']}/{self.prefixes['rgb']}_{self.filenames[sample_id]}").convert('RGB')
        width, height = pilRGB.size
        resize = (300, 0, width-300, height)
        # print(pilRGB.size)
        pilRGB = pilRGB.crop(resize)

        pilIR = self.load_cropped_ir(f"{self.base_folders[sample_id]}/{self.prefixes['ir']}/{self.prefixes['ir']}_{self.filenames[sample_id]}", resize=(width, height))
        # print(pilIR.size)

        imgGT = Image.open(f"{self.base_folders[sample_id]}/{self.prefixes['gt']}/{self.prefixes['gt']}_{self.filenames[sample_id]}").convert('L')
        # print(imgGT.size)
        imgGT = imgGT.resize((width, height), resample=Image.NEAREST)
        imgGT = imgGT.crop(resize)
        pilDep = None

        return pilRGB, pilDep, pilIR, imgGT


class CityscapesDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/cityscapes/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        """
        Initializes the data loader
        :param path: the path to the data
        """
        super().__init__(modalities, resize=resize, name="cityscapes", mode=mode, augment=augment)
        self.path = path

        print(modalities)

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[5]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[5]
            self.class_to_idx['objects'][x[0].lower()] = x[5]
            self.idx_to_obj['objects'][x[4]] = x[5]

        logger.debug(f"{self.name} - idx to obj: {self.idx_to_obj['objects']}")
        logger.debug(f"{self.name} - class to idx: {self.class_to_idx['objects']}")
        logger.debug(f"{self.name} - color to idx: {self.color_to_idx['objects'].values()}")

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        if set == "train":
            self.split_path = 'train/'
        elif set in ["test", "val"]:
            self.split_path = 'val/'
        else:
            self.split_path = '**/'

        cities = {
            "val": ["frankfurt"],
            "test": ["lindau", "munster"]
        }

        self.augment = augment
        self.viz = viz
        self.base_folders = []

        for filepath in glob.glob(self.path + 'gtFine/' + self.split_path + f'**/*labelIds.png'):

            img = '_'.join('/'.join(filepath.split("/")[-2:]).split("_")[:3])
            city = img.split("/")[0]
            base_folder = filepath.split("/")[-3]
            if set in ["train","full"] or city in cities[set]:
                self.filenames.append(img)
                self.base_folders.append(base_folder)
        # print(self.filenames[0])
        # print(len(self.filenames))

        self.color_GT = False


    def get_image_pairs(self, sample_id):

        pilRGB = Image.open(self.path + "leftImg8bit/" + self.base_folders[sample_id] + f"/{self.filenames[sample_id]}_leftImg8bit.png").convert('RGB')
        if not self.depth_completion:
            pilDep = self.load_depth(self.path + "disparity/" + self.base_folders[sample_id] + f"/{self.filenames[sample_id]}_disparity.png", invert=True)
        else:
            pilDep = self.load_depth(self.path + "depthcomp/" + self.base_folders[sample_id] + f"/{self.filenames[sample_id]}_depthcomp.png")
        imgGT = Image.open(self.path + "gtFine/" + self.base_folders[sample_id] + f"/{self.filenames[sample_id]}_gtFine_labelIds.png").convert('L')
        return pilRGB, pilDep, None, imgGT


class KittiDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/kitti/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        """
        Initializes the data loader
        :param path: the path to the data
        """
        super().__init__(modalities, resize=resize, name="kitti", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[4]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[4]
            self.class_to_idx['objects'][x[0].lower()] = x[4]

        # print("class to idx: ", self.class_to_idx['objects'])
        # print("color to idx: ", self.color_to_idx['objects'].values())

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        if set in ["train","test","val","full"]:
            self.split_path = 'training/'
        else:
            self.split_path = 'testing/'

        self.augment = augment
        self.viz = viz

        for img in glob.glob(self.path + "data_semantics/" + self.split_path + "semantic/*.png"):
            img = img.split("/")[-1]
            # print(img)
            self.filenames.append(img)
        # print(self.filenames)
        self.color_GT = False

    def get_image_pairs(self, sample_id):
        pilRGB = Image.open(self.path + "data_scene_flow/" + self.split_path + "image_2/" + f"{self.filenames[sample_id]}").convert('RGB')
        # pilDep = Image.open(self.path + "data_scene_flow/" + self.split_path + "disp_occ_0/" + f"{self.filenames[sample_id]}").convert('L')
        pilDep = self.load_depth(self.path + "data_scene_flow/" + self.split_path + "depthcomp/" + f"{self.filenames[sample_id]}")
        imgGT = Image.open(self.path + "data_semantics/" + self.split_path + "semantic/" + f"{self.filenames[sample_id]}").convert('L')
        return pilRGB, pilDep, None, imgGT

class ThermalVOCDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/thermalworld-voc/dataset/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        """
        Initializes the data loader
        :param path: the path to the data
        """
        super().__init__(modalities, resize=resize, name="thermalvoc", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        if self.mode == "objects":
            self.cls_labels = [0]*len(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[4]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[4]
            self.class_to_idx['objects'][x[0].lower()] = x[4]
            if self.mode == "objects":
                self.cls_labels[x[4]] = x[0].lower()

        logger.debug(f"{self.name} - class to idx: {self.class_to_idx['objects']}")
        logger.debug(f"{self.name} - color to idx: {self.color_to_idx['objects'].values()}")

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])
        logger.debug(self.idx_to_idx["convert"])

        self.path = path + 'train/'

        self.augment = augment
        self.viz = viz

        for img in glob.glob(self.path + 'SegmentationClass/*.png'):
            img = img.split("/")[-1]
            self.filenames.append(img)
        # logger.debug(self.filenames)

        self.color_GT = True

    def get_image_pairs(self, sample_id):
        pilRGB = Image.open(self.path + "ColorImages/" + self.filenames[sample_id]).convert('RGB')
        pilDep = None
        thermal = np.load(self.path + "ThermalImages/" + self.filenames[sample_id].replace(".png",".npy"))
        thermal = (thermal - np.min(thermal))
        thermal = thermal/np.max(thermal)
        pilIR = Image.fromarray(thermal* 255.0).convert('L')

        imgGT = Image.open(self.path + "SegmentationClass/" + self.filenames[sample_id]).convert('RGB')

        return pilRGB, pilDep, pilIR, imgGT


class SynthiaDataLoader(MMDataLoader):

    def __init__(self, resize, set="train", path = "../../datasets/synthia/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        super().__init__(modalities, resize=resize, name="synthia", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        for x in classes:
            x = [int(i) if i.lstrip("-").isdigit() else i for i in x]
            self.idx_to_color['objects'][x[5]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[5]
            self.class_to_idx['objects'][x[0].lower()] = x[5]
            self.idx_to_obj['objects'][x[4]] = x[5]

        logger.debug(f"{self.name} - idx to obj: {self.idx_to_obj['objects']}")
        logger.debug(f"{self.name} - class to idx: {self.class_to_idx['objects']}")
        logger.debug(f"{self.name} - color to idx: {self.color_to_idx['objects'].values()}")

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        self.augment = augment
        self.viz = viz

        for img in glob.glob(self.path + 'SYNTHIA-SEQS-05-SPRING/GT/LABELS/Stereo_Left/' + '**/*.png'):

            img = '/'.join(img.split("/")[-2:])
            self.filenames.append(img)
        # print(self.filenames[0])
        # print(len(self.filenames))

        self.color_GT = False

    def get_image_pairs(self, sample_id):

        pilRGB = Image.open(self.path + "SYNTHIA-SEQS-05-SPRING/RGB/Stereo_Left/" + f"{self.filenames[sample_id]}").convert('RGB')
        pilDep = self.load_depth(self.path + "SYNTHIA-SEQS-05-SPRING/Depth/Stereo_Left/" + f"{self.filenames[sample_id]}")
        imgGT = np.asarray(imageio.imread(self.path + "SYNTHIA-SEQS-05-SPRING/GT/LABELS/Stereo_Left/" + f"{self.filenames[sample_id]}", format='PNG-FI'),dtype=np.uint8)[:,:,0]
        print(np.unique(imgGT))
        return pilRGB, pilDep, None, imgGT


class OwnDataLoader(MMDataLoader):
    def __init__(self, resize, set="train", path = "../../datasets/own/", modalities=["rgb"], mode="affordances", augment=False, viz=False):
        super().__init__(modalities, resize=resize, name="own", mode=mode, augment=augment)
        self.path = path

        classes = np.loadtxt(path + "classes.txt", dtype=str)
        # print(classes)

        for x in classes:
            x = [int(i) if i.isdigit() or "-" in i else i for i in x]
            self.idx_to_color['objects'][x[4]] = tuple([x[1], x[2], x[3]])
            self.color_to_idx['objects'][tuple([x[1], x[2], x[3]])] = x[4]
            self.class_to_idx['objects'][x[0].lower()] = x[4]

        # print("class to idx: ", self.class_to_idx['objects'])
        # print("color to idx: ", self.color_to_idx['objects'].values())

        self.color_to_idx['affordances'], self.idx_to_color['affordances'], self.idx_to_color["convert"], self.idx_to_idx["convert"], self.idx_mappings = self.remap_classes(self.idx_to_color['objects'])

        if set == "train":
            self.split_path = 'training/'
        else:
            self.split_path = 'testing/'

        self.augment = augment
        self.viz = viz

        print(self.path + self.split_path + "rgb/*.jpg")
        for img in glob.glob(self.path + self.split_path + "rgb/*.jpg"):
            img = img.split("/")[-1]
            # print(img)
            self.filenames.append(img)
        print(self.filenames)
        self.color_GT = False
        self.has_affordance_labels = True

    def get_image_pairs(self, sample_id):
        pilRGB = Image.open(self.path + self.split_path + "rgb/" + f"{self.filenames[sample_id]}").convert('RGB')
        width, height = pilRGB.size
        imgGT = Image.new('L', (width, height))
        return pilRGB, None, None, imgGT


if __name__ == '__main__':

    from torch.utils.data import DataLoader, random_split, Subset

    print("Cityscapes dataset")
    train_set = CityscapesDataLoader(set="train", mode="objects", modalities=["rgb"], augment=True)
    train_set = Subset(train_set, indices = range(len(train_set)))
    print("-> train", len(train_set.dataset))
    val_set = CityscapesDataLoader(set="val", mode="objects", modalities=["rgb"], augment=False)
    val_set = Subset(val_set, indices = range(len(val_set)))
    print("-> val", len(val_set.dataset))
    test_set = CityscapesDataLoader(set="test", mode="objects", modalities=["rgb"], augment=False)
    test_set = Subset(test_set, indices = range(len(test_set)))
    print("-> test", len(test_set.dataset))
