"""
Deep Q-Network Architecture
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from drl.config import DRLConfig

class DQN(nn.Module):
    """
    Deep Q-Network for traffic signal control
    """
    def __init__(self, state_dim, action_dim, hidden_layers=None):
        super(DQN, self).__init__()
        
        if hidden_layers is None:
            hidden_layers = DRLConfig.HIDDEN_LAYERS
        
        # Build network layers
        layers = []
        input_dim = state_dim
        
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.ReLU())
            input_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(input_dim, action_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, state):
        """
        Forward pass through network
        Args:
            state: torch.Tensor of shape (batch_size, state_dim)
        Returns:
            Q-values: torch.Tensor of shape (batch_size, action_dim)
        """
        return self.network(state)
