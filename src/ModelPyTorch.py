import matplotlib.pyplot as plt
import pickle
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

    def __init__(self, settings):
        self.settings = settings

    def run_model(self, dataloader):

        # Create CNN
        net = Net()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr=self.settings['learning_rate'], momentum=self.settings['momentum'])

        self.train(net, criterion, optimizer, self.settings['epochs'], dataloader)

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
                if i % 2000 == 1999:  # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0

        print('Finished Training')

        return


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
        x = self.pool4(self.conv5_bn(F.relu(self.conv5b(self.conv4_bn(F.relu(self.conv5a(x)))))))
        x = x.view(-1, 512)
        x = F.relu(self.fc(x))
        return x
