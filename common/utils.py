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


def get_vehicle_mode(vtype):
    """
    Classify vehicle by vType ID from SUMO
    
    Args:
        vtype: Vehicle type ID from SUMO (e.g., 'Volkswagen', 'Raleigh', 'bus', 'Berliner')
    
    Returns:
        str: Vehicle mode ('car', 'bicycle', 'bus', 'pedestrian')
    """
    if vtype == 'Volkswagen':
        return 'car'
    elif vtype == 'Raleigh':
        return 'bicycle'
    elif vtype == 'bus':
        return 'bus'
    elif vtype == 'Berliner':
        return 'pedestrian'
    else:
        return 'car'  # Default fallback
