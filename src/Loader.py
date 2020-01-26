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

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

class Loader(object):

    def __init__(self, settings):
        self.process = Processing(settings)
        self.settings = settings
        self.n = 0

    def load_test_data(self, path):

        image_list = []
        image_file_list = []    # filenames list for image browser
        print(' ')
        for image in os.listdir(path):
            if (os.path.isfile(os.path.join(path, image)) and os.path.getsize(os.path.join(path, image))>0 ) \
                    and image.lower().endswith(img_types): # checking if file of non-zero length exists and belongs to the image type
                image_list.append(self.process.process_image(path+'/'+image))
                image_file_list.append(image)
        if len(image_list) == 0:
            return image_list, image_file_list
        print(f"loaded {len(image_list)} images")
        return self.process.transform(image_list, None)[0], image_file_list


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

        indices = list(range(self.n))
        split = int(np.floor(0.3 * self.n))

        np.random.seed(self.settings['seed'])
        np.random.shuffle(indices)

        train_idx, valid_idx = indices[split:], indices[:split]
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)

        train_loader = torch.utils.data.DataLoader(train_set, batch_size=self.settings['batch_size'], sampler=train_sampler,num_workers=1)
        validation_loader = torch.utils.data.DataLoader(train_set, batch_size=self.settings['batch_size'], sampler=valid_sampler,num_workers=1)

        data_loaders = {"train": train_loader, "val": validation_loader}
        data_lengths = {"train": len(train_idx), "val": len(valid_idx)}

        return train_loader, validation_loader, data_loaders, data_lengths