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
    
    Handles multiple SUMO installation types:
    - Standard: $SUMO_HOME/tools
    - macOS Framework: $SUMO_HOME/share/sumo/tools
    
    Returns:
        str or None: Path to SUMO tools directory if found, None otherwise
    
    Example:
        >>> from common.sumo_utils import setup_sumo_tools
        >>> sumo_tools = setup_sumo_tools()
        >>> if sumo_tools:
        >>>     import traci  # Now available
    """
    if "SUMO_HOME" in os.environ:
        sumo_home = os.environ["SUMO_HOME"]
        
        # Try standard location first
        tools = os.path.join(sumo_home, "tools")
        
        # If not found, try macOS framework location
        if not os.path.exists(tools):
            tools = os.path.join(sumo_home, "share", "sumo", "tools")
        
        # Add to path if it exists
        if os.path.exists(tools) and tools not in sys.path:
            sys.path.append(tools)
            return tools
        elif not os.path.exists(tools):
            print(f"Warning: SUMO tools directory not found at {tools}")
            print(f"SUMO_HOME: {sumo_home}")
            return None
            
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
