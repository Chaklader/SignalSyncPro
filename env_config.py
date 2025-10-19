"""
Environment Configuration Module

Loads environment variables from .env file (similar to dotenv in JS/TS).
Provides centralized access to configuration settings across the codebase.

Usage:
    from env_config import get_run_mode, is_training_mode, is_test_mode

    if is_training_mode():
        # Training-specific code
        pass
    elif is_test_mode():
        # Testing-specific code
        pass
"""

import os
from pathlib import Path

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv

    # Load .env file from project root
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Warning: python-dotenv not installed. Using default values.")
    print("Install with: pip install python-dotenv")


# ============================================================================
# Environment Variables
# ============================================================================


def get_run_mode():
    """
    Get the current run mode from environment variable.

    Returns:
        str: 'training' or 'test'

    Default: 'training'

    Example:
        mode = get_run_mode()
        if mode == 'training':
            print("Running in training mode")
    """
    return os.getenv("RUN_MODE", "training").lower()


def is_training_mode():
    """
    Check if currently in training mode.

    Returns:
        bool: True if RUN_MODE='training'

    Example:
        if is_training_mode():
            agent.train()
    """
    return get_run_mode() == "training"


def is_test_mode():
    """
    Check if currently in test mode.

    Returns:
        bool: True if RUN_MODE='test'

    Example:
        if is_test_mode():
            agent.load_weights()
            agent.evaluate()
    """
    return get_run_mode() == "test"


def get_sumo_gui():
    """
    Get SUMO GUI setting from environment.

    Returns:
        bool: True if GUI should be enabled

    Default: False
    """
    gui_setting = os.getenv("SUMO_GUI", "false").lower()
    return gui_setting in ["true", "1", "yes"]


def get_log_level():
    """
    Get logging level from environment.

    Returns:
        str: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR')

    Default: 'INFO'
    """
    return os.getenv("LOG_LEVEL", "INFO").upper()


# ============================================================================
# Configuration Display
# ============================================================================


def print_config():
    """Print current environment configuration."""
    print("=" * 70)
    print("SignalSyncPro Environment Configuration")
    print("=" * 70)
    print(f"RUN_MODE:    {get_run_mode()}")
    print(f"SUMO_GUI:    {get_sumo_gui()}")
    print(f"LOG_LEVEL:   {get_log_level()}")
    print(
        f"DOTENV:      {'Loaded' if DOTENV_AVAILABLE else 'Not available (using defaults)'}"
    )
    print("=" * 70)


# ============================================================================
# Validation
# ============================================================================


def validate_config():
    """
    Validate environment configuration.

    Raises:
        ValueError: If configuration is invalid
    """
    run_mode = get_run_mode()
    valid_modes = ["training", "test"]

    if run_mode not in valid_modes:
        raise ValueError(
            f"Invalid RUN_MODE: '{run_mode}'. Must be one of: {valid_modes}"
        )


# Auto-validate on import
try:
    validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Falling back to default: RUN_MODE='training'")
    os.environ["RUN_MODE"] = "training"


# ============================================================================
# Export all functions
# ============================================================================

__all__ = [
    "get_run_mode",
    "is_training_mode",
    "is_test_mode",
    "get_sumo_gui",
    "get_log_level",
    "print_config",
    "validate_config",
]
