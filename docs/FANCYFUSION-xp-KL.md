# Freiburg

## V + D

### SSMA

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders single --test_checkpoint "lightning_logs/fusionfusion-ssma16-single-2021-04-20 15-20-freiburg-c3-kl-rgb,depth-epoch=83-val_loss=0.1917.ckpt" --loss_weight

```bash
[INFO] CM IoU - tensor([93.2676, 77.7040, 70.9775])
[INFO] precision tensor([94.3460, 88.7383, 98.3211], dtype=torch.float64) (93.80180696726748) | recall tensor([98.7893, 86.2049, 71.8483], dtype=torch.float64) (85.6141741852646)
Testing: 100%|██████████████████████████████████████████████████████████████████████████████████████| 136/136 [04:44<00:00,  2.09s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9313876628875732,
 'test_acc_w': 0.9230747222900391,
 'test_dist_l1': 0.07119351625442505,
 'test_dist_l2': 0.07635588943958282,
 'test_dist_logl2': 0.02775973454117775,
 'test_dist_mistake_severity': 0.037619899958372116,
 'test_iou': 0.8745157122612}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-ssma16-multi-2021-04-22 02-33-freiburg-c3-kl-rgb,depth-epoch=145-val_loss=0.1714.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([93.6815, 77.9694, 70.9322])
[INFO] precision tensor([94.6184, 88.7113, 98.5732], dtype=torch.float64) (93.96765534748445) | recall tensor([98.9541, 86.5574, 71.6680], dtype=torch.float64) (85.7265010888033)
Testing: 100%|████████████████████████████████| 136/136 [03:30<00:00,  1.55s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9332429766654968,
 'test_acc_w': 0.9241171479225159,
 'test_dist_l1': 0.0682252049446106,
 'test_dist_l2': 0.0711616650223732,
 'test_dist_logl2': 0.025710497051477432,
 'test_dist_mistake_severity': 0.02199360355734825,
 'test_iou': 0.8773732781410217}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-ssma16-late-2021-04-30 18-58-freiburg-c3-kl-rgb,depth-epoch=119-val_loss=0.1430.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([94.2871, 81.8282, 82.0567])
[INFO] precision tensor([95.8443, 90.9104, 97.1103], dtype=torch.float64) (94.62166239356668) | recall tensor([98.3059, 89.1196, 84.1105], dtype=torch.float64) (90.51198689855013)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [02:30<00:00,  1.11s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9464640617370605,
 'test_acc_w': 0.9409504532814026,
 'test_dist_l1': 0.0542394295334816,
 'test_dist_l2': 0.055646445602178574,
 'test_dist_logl2': 0.021511472761631012,
 'test_dist_mistake_severity': 0.01314085815101862,
 'test_iou': 0.900388240814209}
```

### Custom

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders single --test_checkpoint "lightning_logs/fusionfusion-custom16-single-2021-04-20 18-31-freiburg-c3-kl-rgb,depth-epoch=43-val_loss=0.1429.ckpt" --loss_weight --fusion_activ softmax

```bash
[INFO] CM IoU - tensor([94.3308, 81.6555, 80.6822])
[INFO] precision tensor([96.0335, 90.1197, 97.3849], dtype=torch.float64) (94.51272763804161) | recall tensor([98.1550, 89.6843, 82.4689], dtype=torch.float64) (90.10276913391309)
Testing: 100%|██████████████████████████████████████████████████████████████████████████████████████| 136/136 [05:01<00:00,  2.22s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9455978274345398,
 'test_acc_w': 0.9393054246902466,
 'test_dist_l1': 0.05501844733953476,
 'test_dist_l2': 0.056250955909490585,
 'test_dist_logl2': 0.02147301286458969,
 'test_dist_mistake_severity': 0.01132777240127325,
 'test_iou': 0.8989060521125793}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16-multi-2021-04-20 19-24-freiburg-c3-kl-rgb,depth-epoch=141-val_loss=0.1369.ckpt"  --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([94.7388, 82.9838, 81.4231])
[INFO] precision tensor([96.7505, 89.8015, 97.6981], dtype=torch.float64) (94.75003337848898) | recall tensor([97.8524, 91.6181, 83.0157], dtype=torch.float64) (90.82873263703965)
Testing: 100%|█████████████████████████████████████████████████████████████████| 136/136 [03:15<00:00,  1.44s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9492639899253845,
 'test_acc_w': 0.9446205496788025,
 'test_dist_l1': 0.05132059380412102,
 'test_dist_l2': 0.052489787340164185,
 'test_dist_logl2': 0.019895028322935104,
 'test_dist_mistake_severity': 0.011522334069013596,
 'test_iou': 0.9053769707679749}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16-late-2021-04-29 18-41-freiburg-c3-kl-rgb,depth-epoch=39-val_loss=0.1488.ckpt"  --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([94.3708, 81.5557, 79.0987])
[INFO] precision tensor([96.0735, 89.5811, 98.2543], dtype=torch.float64) (94.63631620698436) | recall tensor([98.1566, 90.1024, 80.2261], dtype=torch.float64) (89.49504513435565)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [04:44<00:00,  2.09s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9448168873786926,
 'test_acc_w': 0.9385794401168823,
 'test_dist_l1': 0.055969156324863434,
 'test_dist_l2': 0.05754123255610466,
 'test_dist_logl2': 0.02163451351225376,
 'test_dist_mistake_severity': 0.014244157820940018,
 'test_iou': 0.8975260257720947}
```

## Custom rll

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16rll-multi-2021-04-23 12-22-freiburg-c3-kl-rgb,depth-epoch=102-val_loss=0.1522.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([94.5802, 82.1125, 78.9374])
[INFO] precision tensor([96.5935, 89.0463, 97.8751], dtype=torch.float64) (94.50495446522828) | recall tensor([97.8437, 91.3384, 80.3138], dtype=torch.float64) (89.83196850844925)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [03:06<00:00,  1.37s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9461632966995239,
 'test_acc_w': 0.9408412575721741,
 'test_dist_l1': 0.05455722659826279,
 'test_dist_l2': 0.05599832534790039,
 'test_dist_logl2': 0.020857345312833786,
 'test_dist_mistake_severity': 0.013383997604250908,
 'test_iou': 0.8998969793319702}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16rll-late-2021-04-30 10-43-freiburg-c3-kl-rgb,depth-epoch=104-val_loss=0.1485.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([94.2388, 81.3492, 79.4052])
[INFO] precision tensor([96.0327, 89.4621, 98.1304], dtype=torch.float64) (94.54176087904239) | recall tensor([98.0562, 89.9704, 80.6249], dtype=torch.float64) (89.55049736816272)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [05:21<00:00,  2.37s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9441530108451843,
 'test_acc_w': 0.9376035928726196,
 'test_dist_l1': 0.05662887915968895,
 'test_dist_l2': 0.0581926554441452,
 'test_dist_logl2': 0.02202657051384449,
 'test_dist_mistake_severity': 0.014000543393194675,
 'test_iou': 0.8963139653205872}
```

## V + NIR

### SSMA

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders single --test_checkpoint "lightning_logs/fusionfusion-ssma16-single-2021-04-22 18-56-freiburg-c3-kl-rgb,ir-epoch=118-val_loss=0.1322.ckpt" --loss_weight

```bash
[INFO] CM IoU - tensor([94.8392, 84.1618, 82.2449])
[INFO] precision tensor([96.0142, 92.4601, 97.8517], dtype=torch.float64) (95.44202799461061) | recall tensor([98.7261, 90.3636, 83.7572], dtype=torch.float64) (90.94896954512754)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [02:56<00:00,  1.30s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.952207088470459,
 'test_acc_w': 0.9539870619773865,
 'test_dist_l1': 0.05018988624215126,
 'test_dist_l2': 0.054983850568532944,
 'test_dist_logl2': 0.0206013061106205,
 'test_dist_mistake_severity': 0.05015351623296738,
 'test_iou': 0.9107973575592041}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-ssma16-multi-2021-04-22 17-47-freiburg-c3-kl-rgb,ir-epoch=149-val_loss=0.1251.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([95.5689, 84.8734, 80.8956])
[INFO] precision tensor([97.0032, 91.3888, 97.0436], dtype=torch.float64) (95.14522207831058) | recall tensor([98.4765, 92.2509, 82.9395], dtype=torch.float64) (91.22229192704575)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [03:08<00:00,  1.38s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9549323320388794,
 'test_acc_w': 0.954961895942688,
 'test_dist_l1': 0.04624444618821144,
 'test_dist_l2': 0.0485980249941349,
 'test_dist_logl2': 0.01761517859995365,
 'test_dist_mistake_severity': 0.026111623272299767,
 'test_iou': 0.9151668548583984}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-ssma16-late-2021-04-30 20-05-freiburg-c3-kl-rgb,ir-epoch=119-val_loss=0.1183.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([95.2853, 84.7846, 84.0765])
[INFO] precision tensor([96.9227, 91.6486, 97.1687], dtype=torch.float64) (95.2466525636043) | recall tensor([98.2578, 91.8835, 86.1880], dtype=torch.float64) (92.1097688193799)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [02:33<00:00,  1.13s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9552972912788391,
 'test_acc_w': 0.9547639489173889,
 'test_dist_l1': 0.0453866682946682,
 'test_dist_l2': 0.0467546209692955,
 'test_dist_logl2': 0.017803283408284187,
 'test_dist_mistake_severity': 0.015300570987164974,
 'test_iou': 0.9160788059234619}
```

### Custom

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders single --test_checkpoint "lightning_logs/fusionfusion-custom16-single-2021-04-22 16-04-freiburg-c3-kl-rgb,ir-epoch=120-val_loss=0.1227.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.3012, 84.2461, 82.0962])
[INFO] precision tensor([96.8551, 91.2894, 96.7973], dtype=torch.float64) (94.98062921849879) | recall tensor([98.3444, 91.6102, 84.3884], dtype=torch.float64) (91.44765050341093)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [02:56<00:00,  1.30s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9535983204841614,
 'test_acc_w': 0.9517282247543335,
 'test_dist_l1': 0.04707184433937073,
 'test_dist_l2': 0.048412222415208817,
 'test_dist_logl2': 0.018046030774712563,
 'test_dist_mistake_severity': 0.014443233609199524,
 'test_iou': 0.9129384160041809}

```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16-multi-2021-04-22 14-55-freiburg-c3-kl-rgb,ir-epoch=93-val_loss=0.1186.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.6447, 85.1441, 81.4550])
[INFO] precision tensor([97.3830, 90.6902, 97.8082], dtype=torch.float64) (95.29379856828939) | recall tensor([98.1679, 93.2989, 82.9694], dtype=torch.float64) (91.47874302954384)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [00:53<00:00,  2.54it/s]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9557560086250305,
 'test_acc_w': 0.9557560086250305,
 'test_dist_l1': 0.04503165930509567,
 'test_dist_l2': 0.04660705104470253,
 'test_dist_logl2': 0.017001206055283546,
 'test_dist_mistake_severity': 0.017803482711315155,
 'test_iou': 0.9168466925621033}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16-late-2021-04-29 19-48-freiburg-c3-kl-rgb,ir-epoch=104-val_loss=0.1244.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.4344, 84.5658, 80.8265])
[INFO] precision tensor([97.3533, 89.9856, 98.3051], dtype=torch.float64) (95.21466953919031) | recall tensor([97.9764, 93.3513, 81.9688], dtype=torch.float64) (91.09884588414872)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [05:06<00:00,  2.26s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9538041949272156,
 'test_acc_w': 0.9519256949424744,
 'test_dist_l1': 0.04690946638584137,
 'test_dist_l2': 0.048336777836084366,
 'test_dist_logl2': 0.01771271415054798,
 'test_dist_mistake_severity': 0.015448512509465218,
 'test_iou': 0.9133679866790771}
```


## Custom rll

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16rll-multi-2021-04-23 09-27-freiburg-c3-kl-rgb,ir-epoch=148-val_loss=0.1258.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.3169, 84.5052, 82.1763])
[INFO] precision tensor([96.9198, 91.0575, 97.9184], dtype=torch.float64) (95.29855683635589) | recall tensor([98.2945, 92.1530, 83.6375], dtype=torch.float64) (91.3616600609887)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 136/136 [03:05<00:00,  1.36s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9540855884552002,
 'test_acc_w': 0.9535977840423584,
 'test_dist_l1': 0.0467216856777668,
 'test_dist_l2': 0.04833626747131348,
 'test_dist_logl2': 0.018025588244199753,
 'test_dist_mistake_severity': 0.017582539469003677,
 'test_iou': 0.9138084650039673}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,ir --save --bs 1 --save_xp fusion-rgb,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16rll-late-2021-04-30 12-04-freiburg-c3-kl-rgb,ir-epoch=104-val_loss=0.1262.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.4192, 84.5483, 80.7347])
[INFO] precision tensor([97.4956, 89.6490, 98.2805], dtype=torch.float64) (95.14169601009144) | recall tensor([97.8167, 93.6948, 81.8914], dtype=torch.float64) (91.13431461290276)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [04:35<00:00,  2.02s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9536203742027283,
 'test_acc_w': 0.9516967535018921,
 'test_dist_l1': 0.04704829305410385,
 'test_dist_l2': 0.048385608941316605,
 'test_dist_logl2': 0.01772807538509369,
 'test_dist_mistake_severity': 0.014417062513530254,
 'test_iou': 0.9130036234855652}
---------------------------------
```

## V + D + IR

### SSMA

python3 fusion-test.py --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders single --test_checkpoint "lightning_logs/fusionfusion-ssma16-single-2021-04-24 19-43-freiburg-c3-kl-rgb,depth,ir-epoch=60-val_loss=0.1593.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([93.4948, 80.7195, 80.8209])
[INFO] precision tensor([94.3604, 92.6093, 98.0549], dtype=torch.float64) (95.00820769886028) | recall tensor([99.0284, 86.2774, 82.1377], dtype=torch.float64) (89.14784029043568)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [07:15<00:00,  3.20s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9418808817863464,
 'test_acc_w': 0.9424326419830322,
 'test_dist_l1': 0.06122485175728798,
 'test_dist_l2': 0.06743630021810532,
 'test_dist_logl2': 0.025922482833266258,
 'test_dist_mistake_severity': 0.053437210619449615,
 'test_iou': 0.8925763964653015}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-ssma16-multi-2021-04-24 15-05-freiburg-c3-kl-rgb,depth,ir-epoch=131-val_loss=0.1341.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([94.6043, 83.0012, 84.0250])
[INFO] precision tensor([95.3924, 93.6559, 96.8194], dtype=torch.float64) (95.28924957927956) | recall tensor([99.1343, 87.9458, 86.4101], dtype=torch.float64) (91.1634092287135)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:10<00:00,  1.40s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.950654149055481,
 'test_acc_w': 0.9498316049575806,
 'test_dist_l1': 0.05060974508523941,
 'test_dist_l2': 0.05313757434487343,
 'test_dist_logl2': 0.020610442385077477,
 'test_dist_mistake_severity': 0.025613397359848022,
 'test_iou': 0.907735288143158}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-ssma16-late-2021-04-30 16-29-freiburg-c3-kl-rgb,depth,ir-epoch=64-val_loss=0.1264.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([95.3371, 84.5743, 82.2410])
[INFO] precision tensor([96.9364, 91.0487, 98.1137], dtype=torch.float64) (95.36626211603286) | recall tensor([98.2988, 92.2442, 83.5622], dtype=torch.float64) (91.36841504513171)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:15<00:00,  1.44s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9542930126190186,
 'test_acc_w': 0.9536586999893188,
 'test_dist_l1': 0.046500202268362045,
 'test_dist_l2': 0.048086702823638916,
 'test_dist_logl2': 0.01793714240193367,
 'test_dist_mistake_severity': 0.017355117946863174,
 'test_iou': 0.9142096042633057}
```

### Custom

python3 fusion-test.py --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders single --test_checkpoint "lightning_logs/fusionfusion-custom16-single-2021-04-24 18-29-freiburg-c3-kl-rgb,depth,ir-epoch=103-val_loss=0.1281.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.4166, 84.2346, 80.1194])
[INFO] precision tensor([97.1593, 90.1370, 98.0967], dtype=torch.float64) (95.13098548051411) | recall tensor([98.1549, 92.7869, 81.3845], dtype=torch.float64) (90.77541296416882)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:09<00:00,  1.39s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9529568552970886,
 'test_acc_w': 0.9507584571838379,
 'test_dist_l1': 0.047727227210998535,
 'test_dist_l2': 0.049095433205366135,
 'test_dist_logl2': 0.017887389287352562,
 'test_dist_mistake_severity': 0.014542070217430592,
 'test_iou': 0.9118808507919312}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16-multi-2021-04-24 13-20-freiburg-c3-kl-rgb,depth,ir-epoch=62-val_loss=0.1147.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.5378, 85.6061, 85.4833])
[INFO] precision tensor([97.0633, 92.6208, 96.0788], dtype=torch.float64) (95.25429211091705) | recall tensor([98.3816, 91.8721, 88.5734], dtype=torch.float64) (92.94235223851976)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:08<00:00,  1.39s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9580974578857422,
 'test_acc_w': 0.9579818844795227,
 'test_dist_l1': 0.04256784915924072,
 'test_dist_l2': 0.04389852657914162,
 'test_dist_logl2': 0.016783028841018677,
 'test_dist_mistake_severity': 0.015878261998295784,
 'test_iou': 0.9209979772567749}
-----------------------------------
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16-late-2021-04-29 17-09-freiburg-c3-kl-rgb,depth,ir-epoch=62-val_loss=0.1169.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.2027, 84.9266, 85.7494])
[INFO] precision tensor([96.7817, 92.5290, 96.0674], dtype=torch.float64) (95.12602214912201) | recall tensor([98.3152, 91.1789, 88.8690], dtype=torch.float64) (92.78767630603468)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [05:49<00:00,  2.57s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9560680985450745,
 'test_acc_w': 0.9556142687797546,
 'test_dist_l1': 0.04466266930103302,
 'test_dist_l2': 0.04612419381737709,
 'test_dist_logl2': 0.017899511381983757,
 'test_dist_mistake_severity': 0.016633976250886917,
 'test_iou': 0.9174329042434692}
```

## Custom,rll

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16rll-multi-2021-04-24 16-46-freiburg-c3-kl-rgb,depth,ir-epoch=62-val_loss=0.1102.ckpt" --loss_weight --fusion_activ softmax

```bash
[INFO] CM IoU - tensor([95.7264, 86.2496, 85.9825])
[INFO] precision tensor([97.6446, 92.1615, 95.3133], dtype=torch.float64) (95.03982726477034) | recall tensor([97.9890, 93.0775, 89.7782], dtype=torch.float64) (93.6149172747264)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:20<00:00,  1.47s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9597962498664856,
 'test_acc_w': 0.9603586196899414,
 'test_dist_l1': 0.04079478234052658,
 'test_dist_l2': 0.041976869106292725,
 'test_dist_logl2': 0.015998302027583122,
 'test_dist_mistake_severity': 0.014701212756335735,
 'test_iou': 0.924061119556427}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset freiburg --modalities rgb,depth,ir --save --bs 1 --save_xp fusion-rgb,d,ir --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16rll-late-2021-04-30 14-50-freiburg-c3-kl-rgb,depth,ir-epoch=62-val_loss=0.1150.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([95.3261, 85.2501, 86.0177])
[INFO] precision tensor([96.9222, 92.6060, 95.9736], dtype=torch.float64) (95.16725936289325) | recall tensor([98.3018, 91.4767, 89.2381], dtype=torch.float64) (93.0055250135093)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [03:25<00:00,  1.51s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9570903182029724,
 'test_acc_w': 0.956881582736969,
 'test_dist_l1': 0.04356834664940834,
 'test_dist_l2': 0.044885747134685516,
 'test_dist_logl2': 0.01740398071706295,
 'test_dist_mistake_severity': 0.015350883826613426,
 'test_iou': 0.9192746877670288}
```

# Cityscapes

## Baselines

-- RGB
python3 lightning.py --gpus 0 --num_classes 3 --bs 1 --mode affordances --dataset cityscapes --loss kl --test_checkpoint "lightning_logs/2021-04-09 03-40-cityscapes-c30-kl-rgb-epoch=18-val_loss=0.0918.ckpt" --save --save_xp fusion-rgb,d

--Depthraw
python3 lightning.py --gpus 0 --num_classes 3 --bs 1 --mode affordances --dataset cityscapes --loss kl --test_checkpoint "lightning_logs/2021-04-18 13-12-cityscapes-c30-kl-depthraw-epoch=22-val_loss=0.1251.ckpt" --save --save_xp fusion-rgb,draw --modalities depthraw


--Depthcomp
python3 lightning.py --gpus 0 --num_classes 3 --bs 1 --mode affordances --dataset cityscapes --loss kl --test_checkpoint "lightning_logs/2021-04-17 23-19-cityscapes-c30-kl-depth-epoch=23-val_loss=0.1222.ckpt" --save --save_xp fusion-rgb,d --modalities depth


## V + Draw

### SSMA

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders multi --test_checkpoint "lightning_logs/fusionfusion-ssma16-multi-2021-04-21 23-05-cityscapes-c3-kl-rgb,depthraw-epoch=23-val_loss=0.0883.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([98.2057, 71.7066, 95.0133])
[INFO] precision tensor([98.9061, 82.0908, 98.0469], dtype=torch.float64) (93.01458402771155) | recall tensor([99.2841, 85.0046, 96.8463], dtype=torch.float64) (93.71166447961818)
Testing: 100%|████████████████████████████████| 233/233 [06:02<00:00,  1.56s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9744964241981506,
 'test_acc_w': 0.9796805381774902,
 'test_dist_l1': 0.028959305956959724,
 'test_dist_l2': 0.03587076812982559,
 'test_dist_logl2': 0.0099529679864645,
 'test_dist_mistake_severity': 0.13549986481666565,
 'test_iou': 0.951454758644104}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders single --test_checkpoint "lightning_logs/fusionfusion-ssma16-single-2021-04-20 22-45-cityscapes-c3-kl-rgb,depthraw-epoch=11-val_loss=0.0910.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([98.0832, 67.8026, 93.6397])
[INFO] precision tensor([98.6050, 75.0245, 98.9060], dtype=torch.float64) (90.84515053435638) | recall tensor([99.4634, 87.5678, 94.6197], dtype=torch.float64) (93.88364056002749)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:12<00:00,  1.60s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9690155386924744,
 'test_acc_w': 0.971576988697052,
 'test_dist_l1': 0.03463395684957504,
 'test_dist_l2': 0.04193303734064102,
 'test_dist_logl2': 0.011227413080632687,
 'test_dist_mistake_severity': 0.11778627336025238,
 'test_iou': 0.9422069191932678}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders late --test_checkpoint "lightning_logs/fusionfusion-ssma16-late-2021-05-01 02-36-cityscapes-c3-kl-rgb,depthraw-epoch=21-val_loss=0.0879.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([98.2671, 67.9752, 93.6595])
[INFO] precision tensor([99.0491, 73.7696, 98.7876], dtype=torch.float64) (90.53544714324767) | recall tensor([99.2030, 89.6417, 94.7486], dtype=torch.float64) (94.53109254471315)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [05:43<00:00,  1.47s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9693766236305237,
 'test_acc_w': 0.9713789820671082,
 'test_dist_l1': 0.0334852859377861,
 'test_dist_l2': 0.039209023118019104,
 'test_dist_logl2': 0.010247498750686646,
 'test_dist_mistake_severity': 0.09345358610153198,
 'test_iou': 0.943039059638977}
```

### Custom

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16-multi-2021-04-21 00-22-cityscapes-c3-kl-rgb,depthraw-epoch=23-val_loss=0.0873.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.2418, 68.4958, 93.8710])
[INFO] precision tensor([98.9885, 75.3589, 98.5700], dtype=torch.float64) (90.97247962948174) | recall tensor([99.2380, 88.2644, 95.1670], dtype=torch.float64) (94.2231498945612)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:23<00:00,  1.64s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9702072739601135,
 'test_acc_w': 0.9722357988357544,
 'test_dist_l1': 0.0328991636633873,
 'test_dist_l2': 0.03911207616329193,
 'test_dist_logl2': 0.010336345992982388,
 'test_dist_mistake_severity': 0.10426907986402512,
 'test_iou': 0.9445460438728333}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders single --test_checkpoint "lightning_logs/fusionfusion-custom16-single-2021-04-21 07-16-cityscapes-c3-kl-rgb,depthraw-epoch=2-val_loss=0.0920.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.0910, 70.2256, 94.5367])
[INFO] precision tensor([98.8265, 78.6386, 98.4418], dtype=torch.float64) (91.96899800930018) | recall tensor([99.2469, 86.7798, 95.9728], dtype=torch.float64) (93.99984525112663)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:18<00:00,  1.63s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9722428321838379,
 'test_acc_w': 0.9770115613937378,
 'test_dist_l1': 0.03132832050323486,
 'test_dist_l2': 0.03847062960267067,
 'test_dist_logl2': 0.010617847554385662,
 'test_dist_mistake_severity': 0.12865705788135529,
 'test_iou': 0.9475404024124146}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16-late-2021-04-29 22-42-cityscapes-c3-kl-rgb,depthraw-epoch=13-val_loss=0.0883.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.2124, 67.5911, 93.5051])
[INFO] precision tensor([99.0722, 73.6501, 98.5760], dtype=torch.float64) (90.43277504293337) | recall tensor([99.1241, 89.1495, 94.7854], dtype=torch.float64) (94.35297052786211)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [06:00<00:00,  1.55s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9687408804893494,
 'test_acc_w': 0.9700002074241638,
 'test_dist_l1': 0.034419260919094086,
 'test_dist_l2': 0.040739506483078,
 'test_dist_logl2': 0.01066691242158413,
 'test_dist_mistake_severity': 0.10109435766935349,
 'test_iou': 0.9422619342803955}
```

## Custom RLL

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16rll-multi-2021-04-23 10-38-cityscapes-c3-kl-rgb,depthraw-epoch=13-val_loss=0.0888.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.2434, 67.9050, 93.6971])
[INFO] precision tensor([99.0142, 74.2801, 98.6583], dtype=torch.float64) (90.65085822812549) | recall tensor([99.2139, 88.7792, 94.9064], dtype=torch.float64) (94.2998128257718)
Testing: 100%|██████████████████████████████████████████████████████████████████████| 233/233 [05:58<00:00,  1.54s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9694511890411377,
 'test_acc_w': 0.9709944725036621,
 'test_dist_l1': 0.033514466136693954,
 'test_dist_l2': 0.039445675909519196,
 'test_dist_logl2': 0.010354585014283657,
 'test_dist_mistake_severity': 0.0970773696899414,
 'test_iou': 0.9432992935180664}
 ```

 python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depthraw --save --bs 1 --save_xp fusion-rgb,draw --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16rll-late-2021-04-30 23-13-cityscapes-c3-kl-rgb,depthraw-epoch=13-val_loss=0.0891.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1412, 67.2794, 93.4227])
[INFO] precision tensor([99.0847, 73.1793, 98.5437], dtype=torch.float64) (90.26925147019207) | recall tensor([99.0391, 89.2990, 94.7306], dtype=torch.float64) (94.35620473233257)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [05:45<00:00,  1.48s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9681559801101685,
 'test_acc_w': 0.9694899320602417,
 'test_dist_l1': 0.03513948619365692,
 'test_dist_l2': 0.041730381548404694,
 'test_dist_logl2': 0.010989682748913765,
 'test_dist_mistake_severity': 0.10348714143037796,
 'test_iou': 0.9412776231765747}
 ```

## V + Dcomp

### SSMA

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-ssma16-multi-2021-04-22 00-50-cityscapes-c3-kl-rgb,depth-epoch=15-val_loss=0.0926.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([98.0051, 67.0138, 94.2154])
[INFO] precision tensor([98.5888, 83.3550, 97.0134], dtype=torch.float64) (92.98574961959645) | recall tensor([99.3995, 77.3669, 97.0297], dtype=torch.float64) (91.2653550743594)
Testing: 100%|████████████████████████████████| 233/233 [06:12<00:00,  1.60s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9708035588264465,
 'test_acc_w': 0.9766070246696472,
 'test_dist_l1': 0.033359356224536896,
 'test_dist_l2': 0.041685208678245544,
 'test_dist_logl2': 0.01144882570952177,
 'test_dist_mistake_severity': 0.14258335530757904,
 'test_iou': 0.9444642663002014}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders single --test_checkpoint "lightning_logs/fusionfusion-ssma16-single-2021-04-21 10-37-cityscapes-c3-kl-rgb,depth-epoch=11-val_loss=0.0894.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([97.9988, 67.7790, 93.6209])
[INFO] precision tensor([98.5011, 75.4689, 98.8534], dtype=torch.float64) (90.94115081022119) | recall tensor([99.4823, 86.9311, 94.6487], dtype=torch.float64) (93.68738428837182)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:31<00:00,  1.68s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9688108563423157,
 'test_acc_w': 0.9710447788238525,
 'test_dist_l1': 0.035212695598602295,
 'test_dist_l2': 0.043259840458631516,
 'test_dist_logl2': 0.011689901351928711,
 'test_dist_mistake_severity': 0.1290055811405182,
 'test_iou': 0.9418937563896179}
```

python3 fusion-test.py  --bs 1 --fusion ssma --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-ssma16-late-2021-05-01 00-55-cityscapes-c3-kl-rgb,depth-epoch=22-val_loss=0.0872.ckpt" --loss_weight
```bash
[INFO] CM IoU - tensor([98.1483, 67.8775, 93.5292])
[INFO] precision tensor([98.9911, 74.0485, 98.5967], dtype=torch.float64) (90.54544227795441) | recall tensor([99.1400, 89.0649, 94.7910], dtype=torch.float64) (94.3319966228112)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [05:21<00:00,  1.38s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9687964916229248,
 'test_acc_w': 0.9703645706176758,
 'test_dist_l1': 0.03470006212592125,
 'test_dist_l2': 0.04169318452477455,
 'test_dist_logl2': 0.011020836420357227,
 'test_dist_mistake_severity': 0.11205672472715378,
 'test_iou': 0.942200779914856}
```

## Custom

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16-multi-2021-04-21 14-31-cityscapes-c3-kl-rgb,depth-epoch=5-val_loss=0.0876.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1930, 68.3725, 93.7500])
[INFO] precision tensor([98.9313, 75.0252, 98.6373], dtype=torch.float64) (90.8646233259951) | recall tensor([99.2457, 88.5198, 94.9801], dtype=torch.float64) (94.2485333117285)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:07<00:00,  1.58s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9697316884994507,
 'test_acc_w': 0.9717258810997009,
 'test_dist_l1': 0.033619899302721024,
 'test_dist_l2': 0.04032310098409653,
 'test_dist_logl2': 0.010682874359190464,
 'test_dist_mistake_severity': 0.11072973161935806,
 'test_iou': 0.9436619877815247}
```




python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders single --test_checkpoint "lightning_logs/fusionfusion-custom16-single-2021-04-21 16-17-cityscapes-c3-kl-rgb,depth-epoch=17-val_loss=0.0901.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1752, 69.3024, 94.2064])
[INFO] precision tensor([98.7852, 76.9381, 98.7087], dtype=torch.float64) (91.47733158909452) | recall tensor([99.3749, 87.4733, 95.3818], dtype=torch.float64) (94.0767082411734)
Testing: 100%|█████████████████████████████████████████████████████████████████| 233/233 [06:32<00:00,  1.68s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9712527990341187,
 'test_acc_w': 0.9751651287078857,
 'test_dist_l1': 0.03202430158853531,
 'test_dist_l2': 0.038578473031520844,
 'test_dist_logl2': 0.010415713302791119,
 'test_dist_mistake_severity': 0.11399666219949722,
 'test_iou': 0.9459006786346436}
```


python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16-late-2021-04-30 07-53-cityscapes-c3-kl-rgb,depth-epoch=5-val_loss=0.0878.ckpt" --loss_weight --pretrained_last_layer --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1653, 67.4842, 93.3647])
[INFO] precision tensor([98.8919, 73.6792, 98.7224], dtype=torch.float64) (90.43114368659175) | recall tensor([99.2571, 88.9212, 94.5066], dtype=torch.float64) (94.22828908601844)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [06:11<00:00,  1.60s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.968320369720459,
 'test_acc_w': 0.9695349931716919,
 'test_dist_l1': 0.035195242613554,
 'test_dist_l2': 0.042226433753967285,
 'test_dist_logl2': 0.011085500940680504,
 'test_dist_mistake_severity': 0.1109733060002327,
 'test_iou': 0.9415450096130371}
```


## Custom,RLL

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders multi --test_checkpoint "lightning_logs/fusionfusion-custom16rll-multi-2021-04-24 05-51-cityscapes-c3-kl-rgb,depth-epoch=7-val_loss=0.0880.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1971, 68.4923, 93.8900])
[INFO] precision tensor([98.9395, 75.2437, 98.6587], dtype=torch.float64) (90.94731359544971) | recall tensor([99.2417, 88.4170, 95.1040], dtype=torch.float64) (94.25421596993053)
Testing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [05:47<00:00,  1.49s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9700967073440552,
 'test_acc_w': 0.9729014039039612,
 'test_dist_l1': 0.033069830387830734,
 'test_dist_l2': 0.03940286859869957,
 'test_dist_logl2': 0.010480721481144428,
 'test_dist_mistake_severity': 0.10589193552732468,
 'test_iou': 0.9441050291061401}
```

python3 fusion-test.py  --bs 1 --fusion custom --dataset cityscapes --modalities rgb,depth --save --bs 1 --save_xp fusion-rgb,d --decoders late --test_checkpoint "lightning_logs/fusionfusion-custom16rll-late-2021-04-30 21-32-cityscapes-c3-kl-rgb,depth-epoch=20-val_loss=0.0892.ckpt" --loss_weight --fusion_activ softmax
```bash
[INFO] CM IoU - tensor([98.1091, 68.3072, 93.6320])
[INFO] precision tensor([98.9369, 74.7872, 98.5573], dtype=torch.float64) (90.76049111346478) | recall tensor([99.1544, 88.7432, 94.9331], dtype=torch.float64) (94.27688544723006)
Testing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 233/233 [05:45<00:00,  1.48s/it]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'cm': 0.0,
 'test_acc': 0.9691883325576782,
 'test_acc_w': 0.9716724753379822,
 'test_dist_l1': 0.03455715253949165,
 'test_dist_l2': 0.042048145085573196,
 'test_dist_logl2': 0.011210027150809765,
 'test_dist_mistake_severity': 0.12156099081039429,
 'test_iou': 0.9428227543830872}
```
