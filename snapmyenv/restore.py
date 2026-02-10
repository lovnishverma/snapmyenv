"""Environment restoration functionality."""

import sys
import subprocess
import tempfile
import warnings
import os
from typing import List, Optional

from .models import EnvironmentSnapshot, Package
from .capture import get_snapshot, list_snapshots
from .exceptions import RestoreError


def check_python_version(snapshot: EnvironmentSnapshot) -> None:
    """
    Check if current Python version matches snapshot.
    
    Args:
        snapshot: The environment snapshot to check against.
    """
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    if current_version != snapshot.python_version:
        warnings.warn(
            f"Python version mismatch!\n"
            f"  Snapshot: {snapshot.python_version}\n"
            f"  Current:  {current_version}\n"
            f"Package installation may fail or produce unexpected results.",
            UserWarning,
            stacklevel=2
        )


def batch_install_packages(packages: List[Package], dry_run: bool = False) -> bool:
    """
    Install multiple packages in a single pip call for performance.
    
    Args:
        packages: List of packages to install.
        dry_run: If True, only print what would be installed.
        
    Returns:
        True if installation succeeded, False otherwise.
    """
    if not packages:
        return True

    # Prepare requirements content
    requirements = [f"{pkg.name}=={pkg.version}" for pkg in packages]
    
    if dry_run:
        print("  [DRY RUN] Would install the following packages:")
        for req in requirements:
            print(f"    {req}")
        return True
    
    # Use a temporary file to avoid command line length limits
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_req:
        tmp_req.write("\n".join(requirements))
        tmp_req_path = tmp_req.name

    try:
        print("  Running pip install...")
        # Run pip install -r temp_file
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", tmp_req_path],
            capture_output=True,
            text=True,
            # Timeout scaled by number of packages (30s per package avg)
            timeout=30 + (10 * len(packages)), 
        )
        
        if result.returncode == 0:
            return True
        else:
            # If batch install fails, we warn and provide output
            warnings.warn(f"Batch installation failed: {result.stderr}")
            print(f"Stdout: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        warnings.warn("Timeout during batch installation")
        return False
    except Exception as e:
        warnings.warn(f"Error during batch installation: {e}")
        return False
    finally:
        # Clean up temp file
        if os.path.exists(tmp_req_path):
            os.unlink(tmp_req_path)


def restore_snapshot(snapshot: EnvironmentSnapshot, dry_run: bool = False) -> None:
    """
    Internal logic to restore a specific snapshot object.
    
    Args:
        snapshot: The snapshot object to restore.
        dry_run: If True, preview changes only.
    """
    print(f"{'[DRY RUN] ' if dry_run else ''}Restoring environment '{snapshot.name}'")
    print(snapshot.format_summary())
    print()
    
    # Check Python version
    check_python_version(snapshot)
    
    total = len(snapshot.packages)
    
    if dry_run:
        print(f"Processing {total} packages...")
    else:
        print(f"Installing {total} packages (this may take a moment)...")
    
    # Perform batch installation
    success = batch_install_packages(snapshot.packages, dry_run=dry_run)
    
    print()
    if dry_run:
        print(f"✓ Dry run complete: {total} packages processed")
    else:
        if success:
            print(f"✓ Restoration complete: {total} packages installed successfully.")
        else:
            print("✗ Restoration failed. Check warnings above.")
            raise RestoreError("Failed to install packages.")


def restore(name: str = "default", dry_run: bool = False) -> None:
    """
    Restore environment from a previously captured snapshot in the session.
    
    Args:
        name: Name of the snapshot to restore (default: "default").
        dry_run: If True, show what would be installed without actually installing.
        
    Raises:
        RestoreError: If snapshot not found or restoration fails.
    """
    # Get snapshot from session storage
    snapshot = get_snapshot(name)
    
    if snapshot is None:
        raise RestoreError(
            f"Snapshot '{name}' not found. "
            f"Available snapshots: {', '.join(get_snapshot_names()) or 'none'}"
        )
    
    restore_snapshot(snapshot, dry_run=dry_run)


def restore_from_dict(snapshot_dict: dict, dry_run: bool = False) -> None:
    """
    Restore environment from a snapshot dictionary.
    
    Args:
        snapshot_dict: Dictionary representation of a snapshot.
        dry_run: If True, show what would be installed without actually installing.
        
    Raises:
        RestoreError: If snapshot is invalid or restoration fails.
    """
    try:
        snapshot = EnvironmentSnapshot.from_dict(snapshot_dict)
    except Exception as e:
        raise RestoreError(f"Invalid snapshot data: {e}")
    
    restore_snapshot(snapshot, dry_run=dry_run)


def get_snapshot_names() -> List[str]:
    """
    Get list of available snapshot names.
    
    Returns:
        List of snapshot names.
    """
    return list_snapshots()