"""
snapmyenv - Snapshot and restore Python environments for reproducible notebooks.

A lightweight library for Google Colab and Jupyter users to capture and restore
runtime environments, making notebooks fully reproducible.

Public API:
    capture(name: str = "default") -> dict
        Capture the current Python environment.
    
    restore(name: str = "default", dry_run: bool = False) -> None
        Restore a previously captured environment.
    
    embed(name: str = "default", notebook_path: Optional[str] = None) -> None
        Embed a snapshot into notebook metadata for self-reproducibility.
    
    restore_from_nb(notebook_path: Optional[str] = None, dry_run: bool = False) -> None
        Restore environment from notebook-embedded snapshot.

Example:
    >>> import snapmyenv
    >>> 
    >>> # Capture current environment
    >>> snapshot = snapmyenv.capture("my-project")
    >>> 
    >>> # Later, or on another machine...
    >>> snapmyenv.restore("my-project")
    >>> 
    >>> # Make notebook self-reproducible
    >>> snapmyenv.embed("my-project", "analysis.ipynb")
"""

from .__version__ import __version__, __author__, __license__
from .capture import capture
from .restore import restore
from .notebook import embed, restore_from_nb
from .exceptions import (
    SnapmyenvError,
    CaptureError,
    RestoreError,
    NotebookError,
    ValidationError,
)

# Public API
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    
    # Main functions
    "capture",
    "restore",
    "embed",
    "restore_from_nb",
    
    # Exceptions
    "SnapmyenvError",
    "CaptureError",
    "RestoreError",
    "NotebookError",
    "ValidationError",
]


# Display helpful message on import in interactive environments
def _show_welcome():
    """Show welcome message in interactive environments."""
    try:
        from .colab import is_jupyter
        if is_jupyter():
            print(f"snapmyenv v{__version__} loaded")
            print("Quick start:")
            print("  snapmyenv.capture()        - Snapshot current environment")
            print("  snapmyenv.restore()        - Restore environment")
            print("  snapmyenv.embed()          - Embed in notebook metadata")
            print("  snapmyenv.restore_from_nb() - Restore from notebook")
    except:
        pass


# Only show welcome in interactive mode, not during imports
import sys
if hasattr(sys, 'ps1') or 'IPython' in sys.modules:
    try:
        _show_welcome()
    except:
        pass
