"""Tests for snapenv.restore module."""

import pytest
from snapenv.capture import capture, clear_snapshots
from snapenv.restore import restore, restore_from_dict
from snapenv.exceptions import RestoreError
from snapenv.models import EnvironmentSnapshot, Package


class TestRestore:
    """Tests for restore functionality."""
    
    def setup_method(self):
        """Clear snapshots before each test."""
        clear_snapshots()
    
    def test_restore_not_found(self):
        """Test restoring a non-existent snapshot."""
        with pytest.raises(RestoreError, match="not found"):
            restore("nonexistent")
    
    def test_restore_dry_run(self):
        """Test restore in dry-run mode."""
        # Capture current environment
        capture("test")
        
        # Dry run should not raise errors
        restore("test", dry_run=True)
    
    def test_restore_from_dict(self):
        """Test restoring from a dictionary."""
        # Create a minimal snapshot
        packages = [
            Package(name="pip", version="23.0.0"),
        ]
        
        snapshot = EnvironmentSnapshot(
            name="test",
            python_version="3.10.0",
            platform_system="Linux",
            platform_release="5.15.0",
            platform_machine="x86_64",
            is_colab=False,
            packages=packages,
            timestamp="2024-01-01T00:00:00Z",
            snapenv_version="0.1.0",
        )
        
        # Dry run to avoid actual installation
        restore_from_dict(snapshot.to_dict(), dry_run=True)
    
    def test_restore_from_dict_invalid(self):
        """Test restoring from invalid dictionary."""
        invalid_data = {"invalid": "data"}
        
        with pytest.raises(RestoreError, match="Invalid snapshot"):
            restore_from_dict(invalid_data)