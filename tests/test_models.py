"""Tests for snapenv.models module."""

import pytest
from snapenv.models import Package, EnvironmentSnapshot


class TestPackage:
    """Tests for Package model."""
    
    def test_create_package(self):
        """Test creating a valid package."""
        pkg = Package(name="numpy", version="1.24.0")
        assert pkg.name == "numpy"
        assert pkg.version == "1.24.0"
    
    def test_package_validation(self):
        """Test package validation."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Package(name="", version="1.0.0")
        
        with pytest.raises(ValueError, match="version cannot be empty"):
            Package(name="numpy", version="")
    
    def test_package_to_dict(self):
        """Test package serialization to dict."""
        pkg = Package(name="pandas", version="2.0.0")
        data = pkg.to_dict()
        
        assert data == {"name": "pandas", "version": "2.0.0"}
    
    def test_package_from_dict(self):
        """Test package deserialization from dict."""
        data = {"name": "requests", "version": "2.28.0"}
        pkg = Package.from_dict(data)
        
        assert pkg.name == "requests"
        assert pkg.version == "2.28.0"


class TestEnvironmentSnapshot:
    """Tests for EnvironmentSnapshot model."""
    
    def test_create_snapshot(self):
        """Test creating a valid snapshot."""
        packages = [
            Package(name="numpy", version="1.24.0"),
            Package(name="pandas", version="2.0.0"),
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
        
        assert snapshot.name == "test"
        assert snapshot.python_version == "3.10.0"
        assert len(snapshot.packages) == 2
    
    def test_snapshot_validation(self):
        """Test snapshot validation."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            EnvironmentSnapshot(
                name="",
                python_version="3.10.0",
                platform_system="Linux",
                platform_release="5.15.0",
                platform_machine="x86_64",
                is_colab=False,
                packages=[],
                timestamp="2024-01-01T00:00:00Z",
                snapenv_version="0.1.0",
            )
    
    def test_snapshot_to_dict(self):
        """Test snapshot serialization to dict."""
        packages = [Package(name="numpy", version="1.24.0")]
        
        snapshot = EnvironmentSnapshot(
            name="test",
            python_version="3.10.0",
            platform_system="Linux",
            platform_release="5.15.0",
            platform_machine="x86_64",
            is_colab=True,
            packages=packages,
            timestamp="2024-01-01T00:00:00Z",
            snapenv_version="0.1.0",
        )
        
        data = snapshot.to_dict()
        
        assert data["name"] == "test"
        assert data["python_version"] == "3.10.0"
        assert data["is_colab"] is True
        assert len(data["packages"]) == 1
        assert data["packages"][0]["name"] == "numpy"
    
    def test_snapshot_from_dict(self):
        """Test snapshot deserialization from dict."""
        data = {
            "name": "test",
            "python_version": "3.10.0",
            "platform_system": "Linux",
            "platform_release": "5.15.0",
            "platform_machine": "x86_64",
            "is_colab": False,
            "packages": [
                {"name": "numpy", "version": "1.24.0"},
                {"name": "pandas", "version": "2.0.0"},
            ],
            "timestamp": "2024-01-01T00:00:00Z",
            "snapenv_version": "0.1.0",
            "metadata": {},
        }
        
        snapshot = EnvironmentSnapshot.from_dict(data)
        
        assert snapshot.name == "test"
        assert len(snapshot.packages) == 2
        assert snapshot.packages[0].name == "numpy"
    
    def test_snapshot_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        packages = [Package(name="pytest", version="7.0.0")]
        
        original = EnvironmentSnapshot(
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
        
        json_str = original.to_json()
        restored = EnvironmentSnapshot.from_json(json_str)
        
        assert restored.name == original.name
        assert restored.python_version == original.python_version
        assert len(restored.packages) == len(original.packages)
        assert restored.packages[0].name == original.packages[0].name
    
    def test_get_package_count(self):
        """Test getting package count."""
        packages = [
            Package(name="a", version="1.0.0"),
            Package(name="b", version="2.0.0"),
            Package(name="c", version="3.0.0"),
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
        
        assert snapshot.get_package_count() == 3
    
    def test_get_package(self):
        """Test getting package by name."""
        packages = [
            Package(name="numpy", version="1.24.0"),
            Package(name="pandas", version="2.0.0"),
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
        
        pkg = snapshot.get_package("numpy")
        assert pkg is not None
        assert pkg.name == "numpy"
        assert pkg.version == "1.24.0"
        
        # Case insensitive
        pkg = snapshot.get_package("PANDAS")
        assert pkg is not None
        assert pkg.name == "pandas"
        
        # Not found
        pkg = snapshot.get_package("nonexistent")
        assert pkg is None
    
    def test_format_summary(self):
        """Test formatting snapshot summary."""
        packages = [Package(name="numpy", version="1.24.0")]
        
        snapshot = EnvironmentSnapshot(
            name="my-project",
            python_version="3.10.0",
            platform_system="Linux",
            platform_release="5.15.0",
            platform_machine="x86_64",
            is_colab=True,
            packages=packages,
            timestamp="2024-01-01T00:00:00Z",
            snapenv_version="0.1.0",
        )
        
        summary = snapshot.format_summary()
        
        assert "my-project" in summary
        assert "3.10.0" in summary
        assert "Linux" in summary
        assert "Yes" in summary  # Colab
        assert "1" in summary  # Package count