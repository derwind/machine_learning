# from https://github.com/oreilly-japan/deep-learning-from-scratch-3/blob/master/dezero/datasets.py
import numpy as np
import torch
from torch.utils.data import Dataset

def to_tensor(x):
    return torch.from_numpy(x.astype(np.float32)).clone()

# https://pytorch.org/tutorials/beginner/basics/data_tutorial.html
class SinCurve(Dataset):
    def __init__(self, train=True, transform=None, target_transform=None):
        self.train = train
        self.transform = transform
        self.target_transform = target_transform
        if self.transform is None:
            self.transform = lambda x: x
        if self.target_transform is None:
            self.target_transform = lambda x: x

        self.data = None
        self.label = None
        self.prepare()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.transform(to_tensor(self.data[idx][np.newaxis, :])), \
               self.target_transform(to_tensor(self.label[idx][np.newaxis, :]))

    def prepare(self):
        num_data = 1000
        dtype = np.float64

        x = np.linspace(0, 2 * np.pi, num_data)
        noise_range = (-0.05, 0.05)
        noise = np.random.uniform(noise_range[0], noise_range[1], size=x.shape)
        if self.train:
            y = np.sin(x) + noise
        else:
            y = np.cos(x)
        y = y.astype(dtype)
        self.data = y[:-1][:, np.newaxis]
        self.label = y[1:][:, np.newaxis]
