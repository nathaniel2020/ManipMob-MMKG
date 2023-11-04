import os
from pathlib import Path

import hydra
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
import numpy as np
import random

import torch
import models
from data.dataset_match import CLIPGraspingDataset
from torch.utils.data import DataLoader


@hydra.main(config_path="cfgs", config_name="train")
def main(cfg):
    # set random seeds
    seed = cfg['train']['random_seed']
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    hydra_dir = Path(os.getcwd())
    checkpoint_path = hydra_dir
    last_checkpoint_path = cfg['train']['load_from_last_ckpt']

    checkpoint_callback = ModelCheckpoint(
        monitor=cfg['wandb']['saver']['monitor'],
        dirpath=checkpoint_path,
        filename='{epoch:04d}-{val_acc:.5f}',
        save_top_k=1,
        save_last=True,
    )
    trainer = Trainer(
        gpus=[0],
        fast_dev_run=cfg['debug'],
        checkpoint_callback=checkpoint_callback,
        max_epochs=cfg['train']['max_epochs'],
    )

    # dataset
    train = CLIPGraspingDataset(cfg, mode='train')
    valid = CLIPGraspingDataset(cfg, mode='valid')
    test = CLIPGraspingDataset(cfg, mode='test')

    # model
    model = models.names[cfg['train']['model']](cfg, train, valid)

    # resume epoch and global_steps
    if cfg['train']['load_from_last_ckpt']:
        print(f"Resuming: {last_checkpoint_path}")
        last_ckpt = torch.load(last_checkpoint_path)
        trainer.current_epoch = last_ckpt['epoch']
        trainer.global_step = last_ckpt['global_step']
        model.load_state_dict(last_ckpt["state_dict"])
        del last_ckpt

    trainer.test(
        model=model,
        test_dataloaders=DataLoader(valid, batch_size=cfg['train']['batch_size']),
        ckpt_path='best'
    )

if __name__ == "__main__":
    main()
