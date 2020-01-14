from sched import scheduler

import matplotlib.pyplot as plt
import pickle
import time
import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.optim import lr_scheduler
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.utils import make_grid


class ModelPytorch(object):

    def __init__(self, settings, data_loaders, data_lengths):
        self.settings = settings
        self.data_loaders = data_loaders
        self.data_lengths = data_lengths

    def run_model(self, train_loader, validation_loader):

        # Create CNN
        net = Net()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr=self.settings['learning_rate'], momentum=self.settings['momentum'])

        #self.train(net, criterion, optimizer, self.settings['epochs'], dataloader)
        net_trained = self.train_model(net, criterion, optimizer, self.settings['epochs'])

        return

    def train(self, net, criterion, optimizer, epochs, trainloader):

        for epoch in range(epochs):  # loop over the dataset multiple times

            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 100 == 99:  # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0

        print('Finished Training')

        return

    def train_model(self, net, criterion, optimizer, n_epochs):

        for epoch in range(n_epochs):
            print('Epoch {}/{}'.format(epoch, n_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                if phase == 'train':
                    optimizer = scheduler(optimizer, epoch)
                    net.train(True)  # Set model to training mode
                else:
                    net.train(False)  # Set model to evaluate mode

                running_loss = 0.0

                # Iterate over data.
                for data in self.data_loaders[phase]:

                    # get the input images and their corresponding labels
                    images = data[0]
                    key_pts = data[1]

                    # flatten pts
                    key_pts = key_pts.view(key_pts.size(0), -1)

                    # wrap them in a torch Variable
                    images, key_pts = Variable(images), Variable(key_pts)

                    # convert variables to floats for regression loss
                    key_pts = key_pts.type(torch.FloatTensor)
                    images = images.type(torch.FloatTensor)

                    # forward pass to get outputs
                    output_pts = net(images)

                    # calculate the loss between predicted and target keypoints
                    loss = criterion(output_pts, key_pts)

                    # zero the parameter (weight) gradients
                    optimizer.zero_grad()

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        # update the weights
                        optimizer.step()

                    # print loss statistics
                    running_loss += loss.data[0]

                epoch_loss = running_loss / self.data_lengths[phase]
                print('{} Loss: {:.4f}'.format(phase, epoch_loss))
        return net


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv1_bn = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv2_bn = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.conv3_bn = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.conv4a = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.conv4b = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.conv4_bn = nn.BatchNorm2d(256)
        self.pool4 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.conv5a = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.conv5b = nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.conv5_bn = nn.BatchNorm2d(512)
        self.pool5 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.avg_pool = nn.AvgPool2d(kernel_size=1, stride=1, padding=0)

        self.fc = nn.Linear(512, 15)

    def forward(self, x):
        x = self.pool1(self.conv1_bn(F.relu(self.conv1(x))))
        x = self.pool2(self.conv2_bn(F.relu(self.conv2(x))))
        x = self.pool3(self.conv3_bn(F.relu(self.conv3(x))))
        x = self.pool4(self.conv4_bn(F.relu(self.conv4b(self.conv4_bn(F.relu(self.conv4a(x)))))))
        x = self.pool5(self.conv5_bn(F.relu(self.conv5b(self.conv5_bn(F.relu(self.conv5a(x)))))))
        x = self.avg_pool(x)
        x = x.view(-1, 512)
        x = F.relu(self.fc(x))
        return x
