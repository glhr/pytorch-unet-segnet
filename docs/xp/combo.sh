lightning.py --test_samples 0 --train --bs 8 --lr 0.0001 --optim adam --loss sord --num_classes 30 --mode affordances --dataset combo --dataset_combo freiburg,cityscapes,thermalvoc,synthia,kitti,multispectralseg,freiburgthermal,lostfound --max_epochs 100 --augment --workers 10 --train_checkpoint "lightning_logs/2021-03-29 09-16-cityscapes-c30-kl-rgb-epoch=190-val_loss=0.4310.ckpt" --update_output_layer --ranks 1,2,3 --dist logl2 --dist_alpha 1 --dataset_combo_ntrain 180

python3 lightning.py --dataset combo --dataset_combo freiburg,cityscapes,thermalvoc,synthia,kitti,multispectralseg,freiburgthermal,lostfound --test_set test --bs 1 --save --save_xp test --save --dataset_combo_ntrain 180 --gpus 0

python3 lightning.py --dataset combo --dataset_combo freiburg,cityscapes,thermalvoc,synthia,kitti,multispectralseg,freiburgthermal,lostfound --bs 1 --save --save_xp combotest --save --dataset_combo_ntrain 180 --gpus 0 --test_checkpoint "lightning_logs/2021-05-08 23-36-combo-c30-sord-1,2,3-a1-logl2-rgb-epoch=41-val_loss=0.0057.ckpt"