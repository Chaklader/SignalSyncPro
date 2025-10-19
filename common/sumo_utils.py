"""
SUMO utility functions for path setup and environment configuration.
"""

import os
import sys


def setup_project_paths():
    """
    Add project root to Python path for imports.
    
    This function should be called at the start of any script in subdirectories
    (e.g., run/training/, run/testing/) to ensure proper module imports.
    
    Returns:
        str: Absolute path to project root directory
    
    Example:
        >>> from common.sumo_utils import setup_project_paths
        >>> project_root = setup_project_paths()
    """
    # Get the directory containing this file (common/)
    common_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to get project root
    project_root = os.path.dirname(common_dir)
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    return project_root


def setup_sumo_tools():
    """
    Add SUMO tools to Python path if SUMO_HOME environment variable is set.
    
    This enables importing SUMO's TraCI and other Python tools.
    Should be called after setup_project_paths().
    
    Returns:
        str or None: Path to SUMO tools directory if found, None otherwise
    
    Example:
        >>> from common.sumo_utils import setup_sumo_tools
        >>> sumo_tools = setup_sumo_tools()
        >>> if sumo_tools:
        >>>     import traci  # Now available
    """
    if "SUMO_HOME" in os.environ:
        tools = os.path.join(os.environ["SUMO_HOME"], "tools")
        if tools not in sys.path:
            sys.path.append(tools)
        return tools
    return None


def setup_environment():
    """
    Complete environment setup for SUMO-based scripts.
    
    Combines setup_project_paths() and setup_sumo_tools() into a single call.
    Use this at the start of training/testing scripts for convenience.
    
    Returns:
        tuple: (project_root, sumo_tools_path)
               sumo_tools_path will be None if SUMO_HOME not set
    
    Example:
        >>> from common.sumo_utils import setup_environment
        >>> project_root, sumo_tools = setup_environment()
        >>> # Now all imports work correctly
    """
    project_root = setup_project_paths()
    sumo_tools = setup_sumo_tools()
    return project_root, sumo_tools
