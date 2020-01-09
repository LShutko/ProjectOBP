import os
import numpy as np
from src.Processing import Processing

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.optim import lr_scheduler
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset, SubsetRandomSampler
from torchvision import transforms
from torchvision.utils import make_grid
from torchvision import datasets, transforms, models



class Reader(object):

    def __init__(self, settings):
        self.settings = settings
        self.n = 0

    def load_train_data(self):
        print(f"Loading images")
        image_list = []
        label_list = []

        for plant_label in os.listdir(self.settings['input_directory']):
            print(f"    Loading {plant_label}...")
            image_list_single_label = os.listdir(self.settings['input_directory'] + plant_label)

            for image in image_list_single_label:
                image_list.append(Processing(self.settings).process_image(
                    self.settings['input_directory'] + plant_label + '/' + image))
                label_list.append(plant_label)

        print(f"loaded {len(label_list)} images")

        print(f"Return transformed images and labels")
        self.n = len(image_list)
        return Processing(self.settings).transform(image_list, label_list)

    def load_dataloader(self):
        transform = transforms.Compose([
            transforms.Resize(32),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        train_set = datasets.ImageFolder(root=self.settings['input_directory'], transform=transform)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=self.settings['batch_size'], shuffle=True, num_workers=1)

        # Training samples.
        n_training_samples = round(self.n * 0.7)
        train_sampler = SubsetRandomSampler(np.arange(n_training_samples, dtype=np.int64))

        # Validation samples.
        n_val_samples = round(self.n * 0.3)
        val_sampler = SubsetRandomSampler(np.arange(n_training_samples, n_training_samples + n_val_samples, dtype=np.int64))

        return train_loader

