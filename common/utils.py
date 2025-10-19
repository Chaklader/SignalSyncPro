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
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

    return device


def clean_route_directory(
    route_dir="infrastructure/developed/common/routes", verbose=True
):
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
            if file.endswith(".rou.xml"):
                file_path = os.path.join(route_dir, file)
                os.remove(file_path)
                removed_count += 1
                if verbose:
                    print(f"  Removed: {file}")

    if verbose and removed_count == 0:
        print("  No route files to remove")

    return removed_count


def calculate_traffic_load(traffic_per_hour):
    """
    Calculate traffic load per second for route generation.

    Converts hourly traffic volume to per-second probability for SUMO route generation.
    Automatically applies MINOR_TO_MAJOR_TRAFFIC_RATIO for perpendicular flows.

    Args:
        traffic_per_hour: Number of vehicles/pedestrians per hour

    Returns:
        tuple: (horizontal_load, vertical_load) - Traffic loads per second
               - horizontal_load: Main road traffic per second
               - vertical_load: Minor road traffic per second (scaled by MINOR_TO_MAJOR_TRAFFIC_RATIO)

    Example:
        >>> calculate_traffic_load(400)  # 400/hr main, 25% on minor (from constants)
        (0.1111, 0.0278)  # (main road, minor road) per second
    """
    from constants.constants import MINOR_TO_MAJOR_TRAFFIC_RATIO

    horizontal_load = float(traffic_per_hour) / 3600
    vertical_load = MINOR_TO_MAJOR_TRAFFIC_RATIO * float(traffic_per_hour) / 3600
    
    return horizontal_load, vertical_load


def get_vehicle_mode(vtype):
    """
    Classify vehicle by vType ID from SUMO

    Args:
        vtype: Vehicle type ID from SUMO (e.g., 'Volkswagen', 'Raleigh', 'bus', 'Berliner')

    Returns:
        str: Vehicle mode ('car', 'bicycle', 'bus', 'pedestrian')
    """
    if vtype == "Volkswagen":
        return "car"
    elif vtype == "Raleigh":
        return "bicycle"
    elif vtype == "bus":
        return "bus"
    elif vtype == "Berliner":
        return "pedestrian"
    else:
        return "car"  # Default fallback
