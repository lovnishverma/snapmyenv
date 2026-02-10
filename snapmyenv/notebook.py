"""Jupyter notebook integration for embedding and restoring snapshots."""

import json
import warnings
from pathlib import Path
from typing import Optional

from .models import EnvironmentSnapshot
from .capture import get_snapshot
from .restore import restore_from_dict
from .colab import ensure_jupyter, is_jupyter
from .exceptions import NotebookError


METADATA_KEY = "snapmyenv_snapshot"


def get_notebook_path() -> Optional[Path]:
    """
    Try to determine the current notebook path.
    
    Returns:
        Path to the notebook file, or None if it cannot be determined.
    """
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        
        if ipython is None:
            return None
        
        # Try to get the notebook name from the kernel
        if hasattr(ipython, 'kernel') and hasattr(ipython.kernel, 'session'):
            session = ipython.kernel.session
            if hasattr(session, 'filename'):
                return Path(session.filename)
        
        return None
        
    except Exception:
        return None


def read_notebook(notebook_path: Path) -> dict:
    """
    Read a Jupyter notebook file.
    
    Args:
        notebook_path: Path to the .ipynb file.
        
    Returns:
        Notebook JSON data.
        
    Raises:
        NotebookError: If notebook cannot be read.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise NotebookError(f"Notebook not found: {notebook_path}")
    except json.JSONDecodeError as e:
        raise NotebookError(f"Invalid notebook JSON: {e}")
    except Exception as e:
        raise NotebookError(f"Failed to read notebook: {e}")


def write_notebook(notebook_path: Path, notebook_data: dict) -> None:
    """
    Write a Jupyter notebook file.
    
    Args:
        notebook_path: Path to the .ipynb file.
        notebook_data: Notebook JSON data.
        
    Raises:
        NotebookError: If notebook cannot be written.
    """
    try:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=2)
            f.write('\n')  # Add trailing newline
    except Exception as e:
        raise NotebookError(f"Failed to write notebook: {e}")


def embed(name: str = "default", notebook_path: Optional[str] = None) -> None:
    """
    Embed the captured environment snapshot into notebook metadata.
    
    This makes the notebook self-reproducible. When the notebook is shared,
    others can call restore_from_nb() to recreate the exact environment.
    
    Args:
        name: Name of the snapshot to embed (default: "default").
        notebook_path: Optional path to notebook file. If None, attempts to
                      detect automatically (works in some environments).
        
    Raises:
        NotebookError: If notebook operations fail.
    """
    # Get snapshot
    snapshot = get_snapshot(name)
    if snapshot is None:
        raise NotebookError(
            f"Snapshot '{name}' not found. Call capture('{name}') first."
        )
    
    # Determine notebook path
    if notebook_path is None:
        detected_path = get_notebook_path()
        if detected_path is None:
            raise NotebookError(
                "Could not auto-detect notebook path. "
                "Please provide notebook_path explicitly:\n"
                "  snapmyenv.embed('default', 'my_notebook.ipynb')"
            )
        nb_path = detected_path
    else:
        nb_path = Path(notebook_path)
    
    if not nb_path.exists():
        raise NotebookError(f"Notebook file not found: {nb_path}")
    
    # Read notebook
    notebook_data = read_notebook(nb_path)
    
    # Ensure metadata structure exists
    if "metadata" not in notebook_data:
        notebook_data["metadata"] = {}
    
    # Embed snapshot
    notebook_data["metadata"][METADATA_KEY] = snapshot.to_dict()
    
    # Write notebook
    write_notebook(nb_path, notebook_data)
    
    print(f"✓ Embedded snapshot '{name}' into {nb_path.name}")
    print(f"  Packages: {len(snapshot.packages)}")
    print(f"  Python: {snapshot.python_version}")
    print()
    print("Others can now restore this environment with:")
    print("  import snapmyenv")
    print("  snapmyenv.restore_from_nb()")


def extract_from_notebook(notebook_path: str) -> Optional[EnvironmentSnapshot]:
    """
    Extract embedded snapshot from a notebook file.
    
    Args:
        notebook_path: Path to the .ipynb file.
        
    Returns:
        EnvironmentSnapshot if found, None otherwise.
        
    Raises:
        NotebookError: If notebook cannot be read or snapshot is invalid.
    """
    nb_path = Path(notebook_path)
    
    # Read notebook
    notebook_data = read_notebook(nb_path)
    
    # Extract snapshot from metadata
    metadata = notebook_data.get("metadata", {})
    snapshot_data = metadata.get(METADATA_KEY)
    
    if snapshot_data is None:
        return None
    
    try:
        return EnvironmentSnapshot.from_dict(snapshot_data)
    except Exception as e:
        raise NotebookError(f"Invalid embedded snapshot: {e}")


def restore_from_nb(notebook_path: Optional[str] = None, dry_run: bool = False) -> None:
    """
    Restore environment from snapshot embedded in notebook metadata.
    
    Args:
        notebook_path: Optional path to notebook file. If None, attempts to
                      detect automatically (works in some environments).
        dry_run: If True, show what would be installed without actually installing.
        
    Raises:
        NotebookError: If notebook operations fail or no snapshot found.
    """
    # Determine notebook path
    if notebook_path is None:
        detected_path = get_notebook_path()
        if detected_path is None:
            raise NotebookError(
                "Could not auto-detect notebook path. "
                "Please provide notebook_path explicitly:\n"
                "  snapmyenv.restore_from_nb('my_notebook.ipynb')"
            )
        nb_path = detected_path
    else:
        nb_path = Path(notebook_path)
    
    if not nb_path.exists():
        raise NotebookError(f"Notebook file not found: {nb_path}")
    
    # Extract snapshot
    snapshot = extract_from_notebook(str(nb_path))
    
    if snapshot is None:
        raise NotebookError(
            f"No snapmyenv snapshot found in {nb_path.name}\n"
            f"The notebook author needs to call snapmyenv.embed() first."
        )
    
    print(f"Found embedded snapshot in {nb_path.name}")
    
    # Restore from snapshot
    restore_from_dict(snapshot.to_dict(), dry_run=dry_run)