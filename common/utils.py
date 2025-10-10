"""
Common utility functions for DRL training
"""
import torch


def get_device(device=None):
    """
    Auto-detect best available device for PyTorch
    
    Priority: MPS (Mac GPU) > CUDA (NVIDIA GPU) > CPU
    
    Args:
        device: Optional device string ('mps', 'cuda', 'cpu')
                If None, auto-detects best available device
    
    Returns:
        str: Device string ('mps', 'cuda', or 'cpu')
    """
    if device is None:
        if torch.backends.mps.is_available():
            device = 'mps'
        elif torch.cuda.is_available():
            device = 'cuda'
        else:
            device = 'cpu'
    
    return device
