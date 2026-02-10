"""Environment capture functionality."""

import sys
import platform
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional
import warnings

from .models import EnvironmentSnapshot, Package
from .colab import is_colab
from .exceptions import CaptureError
from .__version__ import __version__


# Global storage for snapshots in the current session
_SNAPSHOTS: Dict[str, EnvironmentSnapshot] = {}


def get_installed_packages() -> List[Package]:
    """
    Get list of all installed packages with versions.
    
    Returns:
        List of Package objects.
        
    Raises:
        CaptureError: If package list cannot be retrieved.
    """
    try:
        # Use pip list --format=json for reliable parsing
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        
        import json
        packages_data = json.loads(result.stdout)
        
        packages = []
        for pkg_data in packages_data:
            try:
                packages.append(Package(
                    name=pkg_data["name"],
                    version=pkg_data["version"]
                ))
            except (KeyError, ValueError) as e:
                warnings.warn(f"Skipping malformed package entry: {pkg_data}")
                continue
        
        return packages
        
    except subprocess.TimeoutExpired:
        raise CaptureError("Timeout while retrieving package list")
    except subprocess.CalledProcessError as e:
        raise CaptureError(f"Failed to retrieve package list: {e.stderr}")
    except Exception as e:
        raise CaptureError(f"Unexpected error retrieving packages: {e}")


def capture(name: str = "default", metadata: Optional[Dict[str, str]] = None) -> dict:
    """
    Capture the current Python environment.
    
    Args:
        name: Name for this snapshot (default: "default").
        metadata: Optional additional metadata to store with snapshot.
        
    Returns:
        Dictionary representation of the captured environment.
        
    Raises:
        CaptureError: If capture fails.
    """
    if not name or not isinstance(name, str):
        raise CaptureError("Snapshot name must be a non-empty string")
    
    try:
        # Get installed packages
        packages = get_installed_packages()
        
        # Create snapshot
        # FIX: Use datetime.now(timezone.utc) instead of deprecated utcnow()
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        snapshot = EnvironmentSnapshot(
            name=name,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            platform_system=platform.system(),
            platform_release=platform.release(),
            platform_machine=platform.machine(),
            is_colab=is_colab(),
            packages=packages,
            timestamp=timestamp,
            snapmyenv_version=__version__,
            metadata=metadata or {},
        )
        
        # Store in session
        _SNAPSHOTS[name] = snapshot
        
        # Return dictionary representation
        snapshot_dict = snapshot.to_dict()
        
        print(f"✓ Captured environment '{name}'")
        print(f"  Python: {snapshot.python_version}")
        print(f"  Platform: {snapshot.platform_system}")
        print(f"  Packages: {len(packages)}")
        print(f"  Colab: {'Yes' if snapshot.is_colab else 'No'}")
        
        return snapshot_dict
        
    except Exception as e:
        if isinstance(e, CaptureError):
            raise
        raise CaptureError(f"Failed to capture environment: {e}")


def get_snapshot(name: str = "default") -> Optional[EnvironmentSnapshot]:
    """
    Get a stored snapshot by name.
    
    Args:
        name: Name of the snapshot to retrieve.
        
    Returns:
        EnvironmentSnapshot object or None if not found.
    """
    return _SNAPSHOTS.get(name)


def list_snapshots() -> List[str]:
    """
    List all stored snapshot names in the current session.
    
    Returns:
        List of snapshot names.
    """
    return list(_SNAPSHOTS.keys())


def clear_snapshots() -> None:
    """Clear all stored snapshots from the current session."""
    _SNAPSHOTS.clear()