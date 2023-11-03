import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self, input_channels, num_actions):
        super(Model, self).__init()

        # Define the convolutional layers for processing the board state
        self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)

        # Define fully connected layers for policy and value prediction
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, num_actions)
        self.fc3 = nn.Linear(512, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))

        x = x.view(x.size(0), -1)  # Flatten the output for the fully connected layers

        policy = F.log_softmax(self.fc2(F.relu(self.fc1(x)), dim=1))
        value = torch.tanh(self.fc3(x))

        return policy, value
