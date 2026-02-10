"""Environment restoration functionality."""

import sys
import subprocess
import warnings
from typing import List, Optional, Set

from .models import EnvironmentSnapshot, Package
from .capture import get_snapshot
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


def install_package(package: Package, dry_run: bool = False) -> bool:
    """
    Install a single package.
    
    Args:
        package: Package to install.
        dry_run: If True, only print what would be installed.
        
    Returns:
        True if installation succeeded (or dry_run), False otherwise.
    """
    package_spec = f"{package.name}=={package.version}"
    
    if dry_run:
        print(f"  [DRY RUN] Would install: {package_spec}")
        return True
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", package_spec],
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        if result.returncode == 0:
            return True
        else:
            warnings.warn(f"Failed to install {package_spec}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        warnings.warn(f"Timeout installing {package_spec}")
        return False
    except Exception as e:
        warnings.warn(f"Error installing {package_spec}: {e}")
        return False


def restore(name: str = "default", dry_run: bool = False) -> None:
    """
    Restore environment from a previously captured snapshot.
    
    Args:
        name: Name of the snapshot to restore (default: "default").
        dry_run: If True, show what would be installed without actually installing.
        
    Raises:
        RestoreError: If snapshot not found or restoration fails.
        
    Example:
        >>> import snapmyenv
        >>> snapmyenv.restore("my-project")
        >>> # Or preview changes:
        >>> snapmyenv.restore("my-project", dry_run=True)
    """
    # Get snapshot from session storage
    snapshot = get_snapshot(name)
    
    if snapshot is None:
        raise RestoreError(
            f"Snapshot '{name}' not found. "
            f"Available snapshots: {', '.join(get_snapshot_names()) or 'none'}"
        )
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Restoring environment '{name}'")
    print(snapshot.format_summary())
    print()
    
    # Check Python version
    check_python_version(snapshot)
    
    # Install packages
    total = len(snapshot.packages)
    succeeded = 0
    failed = 0
    
    if dry_run:
        print(f"Would install {total} packages:")
    else:
        print(f"Installing {total} packages...")
    
    for i, package in enumerate(snapshot.packages, 1):
        if not dry_run:
            print(f"  [{i}/{total}] {package.name}=={package.version}", end="")
        
        success = install_package(package, dry_run=dry_run)
        
        if success:
            succeeded += 1
            if not dry_run:
                print(" ✓")
        else:
            failed += 1
            if not dry_run:
                print(" ✗")
    
    print()
    if dry_run:
        print(f"✓ Dry run complete: {total} packages would be installed")
    else:
        print(f"✓ Restoration complete: {succeeded} succeeded, {failed} failed")
        
        if failed > 0:
            warnings.warn(
                f"{failed} packages failed to install. "
                f"Check warnings above for details.",
                UserWarning
            )


def restore_from_dict(snapshot_dict: dict, dry_run: bool = False) -> None:
    """
    Restore environment from a snapshot dictionary.
    
    Args:
        snapshot_dict: Dictionary representation of a snapshot.
        dry_run: If True, show what would be installed without actually installing.
        
    Raises:
        RestoreError: If snapshot is invalid or restoration fails.
        
    Example:
        >>> import snapmyenv
        >>> snapshot = snapmyenv.capture("temp")
        >>> snapmyenv.restore_from_dict(snapshot)
    """
    try:
        snapshot = EnvironmentSnapshot.from_dict(snapshot_dict)
    except Exception as e:
        raise RestoreError(f"Invalid snapshot data: {e}")
    
    # Temporarily store snapshot for restoration
    from .capture import _SNAPSHOTS
    temp_name = f"_restore_temp_{id(snapshot_dict)}"
    _SNAPSHOTS[temp_name] = snapshot
    
    try:
        restore(temp_name, dry_run=dry_run)
    finally:
        # Clean up temporary snapshot
        _SNAPSHOTS.pop(temp_name, None)


def get_snapshot_names() -> List[str]:
    """
    Get list of available snapshot names.
    
    Returns:
        List of snapshot names.
    """
    from .capture import list_snapshots
    return list_snapshots()