"""Data models for environment snapshots."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional
import sys
import platform
import json


@dataclass
class Package:
    """Represents an installed Python package."""
    name: str
    version: str
    
    def __post_init__(self):
        """Validate package data."""
        if not self.name:
            raise ValueError("Package name cannot be empty")
        if not self.version:
            raise ValueError("Package version cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {"name": self.name, "version": self.version}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Package":
        """Create from dictionary."""
        return cls(name=data["name"], version=data["version"])


@dataclass
class EnvironmentSnapshot:
    """Complete snapshot of a Python environment."""
    
    name: str
    python_version: str
    platform_system: str
    platform_release: str
    platform_machine: str
    is_colab: bool
    packages: List[Package]
    timestamp: str
    snapmyenv_version: str
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate snapshot data."""
        if not self.name:
            raise ValueError("Snapshot name cannot be empty")
        if not self.python_version:
            raise ValueError("Python version cannot be empty")
        if not isinstance(self.packages, list):
            raise ValueError("Packages must be a list")
    
    def to_dict(self) -> dict:
        """Convert snapshot to dictionary."""
        return {
            "name": self.name,
            "python_version": self.python_version,
            "platform_system": self.platform_system,
            "platform_release": self.platform_release,
            "platform_machine": self.platform_machine,
            "is_colab": self.is_colab,
            "packages": [pkg.to_dict() for pkg in self.packages],
            "timestamp": self.timestamp,
            "snapmyenv_version": self.snapmyenv_version,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EnvironmentSnapshot":
        """Create snapshot from dictionary."""
        packages = [Package.from_dict(pkg) for pkg in data["packages"]]
        return cls(
            name=data["name"],
            python_version=data["python_version"],
            platform_system=data["platform_system"],
            platform_release=data["platform_release"],
            platform_machine=data["platform_machine"],
            is_colab=data["is_colab"],
            packages=packages,
            timestamp=data["timestamp"],
            snapmyenv_version=data["snapmyenv_version"],
            metadata=data.get("metadata", {}),
        )
    
    def to_json(self, indent: int = 2) -> str:
        """Convert snapshot to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> "EnvironmentSnapshot":
        """Create snapshot from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_package_count(self) -> int:
        """Get number of packages in snapshot."""
        return len(self.packages)
    
    def get_package(self, name: str) -> Optional[Package]:
        """Get package by name."""
        for pkg in self.packages:
            if pkg.name.lower() == name.lower():
                return pkg
        return None
    
    def format_summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            f"Snapshot: {self.name}",
            f"Created: {self.timestamp}",
            f"Python: {self.python_version}",
            f"Platform: {self.platform_system} {self.platform_release} ({self.platform_machine})",
            f"Colab: {'Yes' if self.is_colab else 'No'}",
            f"Packages: {self.get_package_count()}",
        ]
        return "\n".join(lines)