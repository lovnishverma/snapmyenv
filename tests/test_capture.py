"""Tests for snapmyenv.capture module."""

import pytest
from snapmyenv.capture import capture, get_snapshot, list_snapshots, clear_snapshots
from snapmyenv.exceptions import CaptureError


class TestCapture:
    """Tests for capture functionality."""
    
    def setup_method(self):
        """Clear snapshots before each test."""
        clear_snapshots()
    
    def test_capture_basic(self):
        """Test basic environment capture."""
        snapshot_dict = capture("test")
        
        assert snapshot_dict["name"] == "test"
        assert "python_version" in snapshot_dict
        assert "platform_system" in snapshot_dict
        assert "packages" in snapshot_dict
        assert isinstance(snapshot_dict["packages"], list)
        assert len(snapshot_dict["packages"]) > 0
    
    def test_capture_default_name(self):
        """Test capture with default name."""
        snapshot_dict = capture()
        
        assert snapshot_dict["name"] == "default"
    
    def test_capture_with_metadata(self):
        """Test capture with custom metadata."""
        metadata = {"project": "test", "author": "user"}
        snapshot_dict = capture("test", metadata=metadata)
        
        assert snapshot_dict["metadata"]["project"] == "test"
        assert snapshot_dict["metadata"]["author"] == "user"
    
    def test_capture_invalid_name(self):
        """Test capture with invalid name."""
        with pytest.raises(CaptureError, match="non-empty string"):
            capture("")
        
        with pytest.raises(CaptureError):
            capture(None)
    
    def test_get_snapshot(self):
        """Test retrieving a captured snapshot."""
        capture("test")
        
        snapshot = get_snapshot("test")
        assert snapshot is not None
        assert snapshot.name == "test"
        
        # Non-existent snapshot
        snapshot = get_snapshot("nonexistent")
        assert snapshot is None
    
    def test_list_snapshots(self):
        """Test listing captured snapshots."""
        assert list_snapshots() == []
        
        capture("first")
        assert list_snapshots() == ["first"]
        
        capture("second")
        snapshots = list_snapshots()
        assert len(snapshots) == 2
        assert "first" in snapshots
        assert "second" in snapshots
    
    def test_clear_snapshots(self):
        """Test clearing all snapshots."""
        capture("test1")
        capture("test2")
        assert len(list_snapshots()) == 2
        
        clear_snapshots()
        assert list_snapshots() == []
    
    def test_capture_overwrites_existing(self):
        """Test that capturing with same name overwrites."""
        snapshot1 = capture("test")
        snapshot2 = capture("test")
        
        # Should only have one snapshot with this name
        snapshots = list_snapshots()
        assert snapshots.count("test") == 1