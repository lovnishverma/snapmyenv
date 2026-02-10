"""Google Colab detection and utilities."""

import sys
from typing import Optional


def is_colab() -> bool:
    """
    Detect if running in Google Colab.
    
    Returns:
        True if running in Google Colab, False otherwise.
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def is_jupyter() -> bool:
    """
    Detect if running in any Jupyter environment.
    
    Returns:
        True if running in Jupyter (including Colab), False otherwise.
    """
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython is None:
            return False
        
        # Check if we're in a notebook kernel
        return 'IPKernelApp' in ipython.config
    except (ImportError, AttributeError):
        return False


def get_environment_type() -> str:
    """
    Get the type of environment we're running in.
    
    Returns:
        One of: 'colab', 'jupyter', 'python'
    """
    if is_colab():
        return 'colab'
    elif is_jupyter():
        return 'jupyter'
    else:
        return 'python'


def get_colab_version() -> Optional[str]:
    """
    Get Google Colab version if available.
    
    Returns:
        Colab version string or None if not in Colab.
    """
    if not is_colab():
        return None
    
    try:
        import google.colab
        # Colab doesn't expose version directly, so we return a generic indicator
        return "colab"
    except ImportError:
        return None


def ensure_jupyter() -> None:
    """
    Ensure we're running in a Jupyter environment.
    
    Raises:
        RuntimeError: If not running in Jupyter.
    """
    if not is_jupyter():
        raise RuntimeError(
            "This function must be called from a Jupyter notebook environment. "
            f"Current environment: {get_environment_type()}"
        )