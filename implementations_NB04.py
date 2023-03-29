import numpy as np
import random
random.seed(46)

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

"""
1) Neural nets
"""

########### Neural net ###############################
def separation_validation(X, y, percent=0.8):
    """
    Separates de train data into train and validation set 
    
    Args:
    X: input data
    y: output values
    percent: percentage of the data in the train set 
    
    """
    data_l=X.shape[0]
    choice = np.linspace(0,data_l-1,data_l, dtype=int)
    np.random.shuffle(choice)

    num_train = int(np.floor(data_l * percent))
    num_val = data_l - num_train

    X_train= X[choice[0:num_train],:]
    X_val = X[choice[num_train:],:]
    
    y_train= y[choice[0:num_train]]
    y_val = y[choice[num_train:]]
    return X_train, X_val, y_train, y_val

def separation_test_day(X, y):
    """
    Separates the train data into train and validation set according to the days 
    1st day: 2470
    2nd day: 2375
    3rd day: 2070
    4th day: 2514
    
    Args:
    X: input data
    y: output values
    
    """
    monday=2470 ; tuesday= 2375 ; wednesday= 2070 ; thursday= 2514
    data_l= monday + tuesday + wednesday
    index=0
    
    for veh in range(len(X)): 
        if X[veh,0]>data_l:
            index=veh
            break
            
    X_train= X[0:index,:] ; X_val = X[index:,:]
    y_train= y[0:index,:] ; y_val = y[index:,:]
    
    return X_train, X_val, y_train, y_val
class LossMetric:
    """Keeps track of the loss over an epoch"""

    def __init__(self) -> None:
        self.running_loss = 0
        self.count = 0

    def update(self, loss: float, batch_size: int) -> None:
        self.running_loss += loss * batch_size
        self.count += batch_size

    def compute(self) -> float:
        return self.running_loss / self.count

    def reset(self) -> None:
        self.running_loss = 0
        self.count = 0
        
class FiveLayerNet(nn.Module):
    """5-Layer neural net"""
    """4 Hidden-Layer neural net"""
    
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(18, 300) #change the first size
        self.fc2 = nn.Linear(300, 300)
        self.fc3 = nn.Linear(300, 1000)
        self.fc4 = nn.Linear(1000, 300)
        self.fc5 = nn.Linear(300, 1)
        self.norm1= nn.BatchNorm1d(num_features=18, eps=1e-08, momentum=0.1)
        self.norm2= nn.BatchNorm1d(num_features=300, eps=1e-08, momentum=0.1)
        self.norm3= nn.BatchNorm1d(num_features=300, eps=1e-08, momentum=0.1)
        self.norm4= nn.BatchNorm1d(num_features=1000, eps=1e-08, momentum=0.1)
        self.drop = nn.Dropout(p=0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.norm1(x)
        x = F.relu(self.fc1(x))
        x = self.norm2(x)
        x = F.relu(self.fc2(x))
        x = self.norm3(x)
        x = self.drop(x)
        x = F.relu(self.fc3(x))
        x = self.norm4(x)
        x = F.relu(self.fc4(x))
        out = self.fc5(x)
        return out

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        pred = self.forward(x)
        return pred
    
class ThreeLayerNet(nn.Module):
    """3-Layer neural net"""
    """2 Hidden-Layer neural net"""
    
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(18, 300) #change the first size
        self.fc2 = nn.Linear(300, 300)
        self.fc3 = nn.Linear(300, 1)
        self.norm1= nn.BatchNorm1d(num_features=18, eps=1e-08, momentum=0.1)
        self.norm2= nn.BatchNorm1d(num_features=300, eps=1e-08, momentum=0.1)
        self.drop = nn.Dropout(p=0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.norm1(x)
        x = F.relu(self.fc1(x))
        x = self.norm2(x)
        x = self.drop(x)
        x = F.relu(self.fc2(x))
        out = self.fc3(x)
        return out

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        pred = self.forward(x)
        return pred