"""
Common utility functions for DRL training
"""
import torch
import os


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


def clean_route_directory(route_dir="infrastructure/developed/common/routes", verbose=True):
    """
    Clean all .rou.xml files from the route directory.
    
    Used before training/testing to ensure fresh start
    with conflicting vehicle type definitions.
    
    Args:
        route_dir: Path to the route directory (default: infrastructure/developed/common/routes)
        verbose: If True, print removal messages (default: True)
    
    Returns:
        int: Number of files removed
    """
    removed_count = 0
    
    if verbose:
        print(f"Cleaning route directory: {route_dir}")
    
    if os.path.exists(route_dir):
        for file in os.listdir(route_dir):
            if file.endswith('.rou.xml'):
                file_path = os.path.join(route_dir, file)
                os.remove(file_path)
                removed_count += 1
                if verbose:
                    print(f"  Removed: {file}")
    
    if verbose and removed_count == 0:
        print("  No route files to remove")
    
    return removed_count


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
