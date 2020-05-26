import os

import torch as t
import torch.utils.data
import torchvision as tv


def load_data(dataset, data_dir, batch_size, workers, val_split=0.):
    if val_split < 0 or val_split >= 1:
        raise ValueError('val_split should be in the range of [0, 1) but got %.3f' % val_split)

    if dataset == 'imagenet':
        train_transform = tv.transforms.Compose([
            tv.transforms.RandomResizedCrop(224),
            tv.transforms.RandomHorizontalFlip(),
            tv.transforms.ToTensor(),
            tv.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
        ])

        val_transform = tv.transforms.Compose([
            tv.transforms.Resize(256),
            tv.transforms.CenterCrop(224),
            tv.transforms.ToTensor(),
            tv.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
        ])

        train_folder = tv.datasets.ImageFolder(
            root=os.path.join(data_dir, 'train'), transform=train_transform)
        val_folder = tv.datasets.ImageFolder(
            root=os.path.join(data_dir, 'val'), transform=val_transform)

        val_len = int(val_split * len(train_folder))
        train_len = len(train_folder) - val_len

        val_loader = None
        if val_split != 0:
            train_set, val_set = t.utils.data.random_split(train_folder, [train_len, val_len])
            val_loader = t.utils.data.DataLoader(
                val_set, batch_size, num_workers=workers, pin_memory=True)
        else:
            train_set = train_folder

        train_loader = t.utils.data.DataLoader(
            train_set, batch_size, shuffle=True, num_workers=workers, pin_memory=True)
        test_loader = t.utils.data.DataLoader(
            val_folder, batch_size, num_workers=workers, pin_memory=True)

        return train_loader, val_loader or test_loader, test_loader
    else:
        raise ValueError('load_data does not support dataset %s' % dataset)
