# snapenv 📸

**Snapshot and restore Python environments for reproducible notebooks**

`snapenv` is a lightweight library designed for Google Colab and Jupyter users to capture and restore runtime environments, making notebooks fully reproducible. Share your notebooks with confidence knowing others can recreate your exact environment.

[![PyPI version](https://badge.fury.io/py/snapenv.svg)](https://badge.fury.io/py/snapenv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📸 **Capture environments** - Snapshot Python version, OS, and all installed packages
- 🔄 **Restore environments** - Recreate exact package versions from snapshots
- 📓 **Notebook integration** - Embed snapshots directly in `.ipynb` metadata
- 🌐 **Colab-friendly** - Designed for Google Colab and local Jupyter
- 🪶 **Zero dependencies** - No external dependencies beyond Python stdlib
- 🛡️ **Production-ready** - Clean error handling, validation, and logging

## Installation

```bash
pip install snapenv
```

## Quick Start

### Basic Usage

```python
import snapenv

# Capture your current environment
snapshot = snapenv.capture("my-analysis")
# ✓ Captured environment 'my-analysis'
#   Python: 3.10.12
#   Platform: Linux
#   Packages: 147
#   Colab: Yes

# Later, restore the exact environment
snapenv.restore("my-analysis")
# Installing 147 packages...
# ✓ Restoration complete: 147 succeeded, 0 failed
```

### Make Notebooks Self-Reproducible

Embed your environment snapshot directly into your notebook:

```python
# In your notebook:
import snapenv

# 1. Capture environment
snapenv.capture("v1")

# 2. Embed in notebook metadata
snapenv.embed("v1", "my_analysis.ipynb")
# ✓ Embedded snapshot 'v1' into my_analysis.ipynb

# Now anyone opening your notebook can restore:
snapenv.restore_from_nb("my_analysis.ipynb")
```

## Google Colab Example

Perfect for sharing reproducible analyses on Colab:

```python
# At the top of your Colab notebook:
!pip install snapenv

import snapenv

# Capture your carefully crafted environment
snapenv.capture("colab-analysis-v1")

# Save it to your notebook
snapenv.embed("colab-analysis-v1", "/content/drive/MyDrive/analysis.ipynb")
```

When someone else opens your notebook:

```python
import snapenv

# Restore the exact environment
snapenv.restore_from_nb("/content/drive/MyDrive/analysis.ipynb")
```

## API Reference

### `capture(name: str = "default", metadata: dict = None) -> dict`

Capture the current Python environment.

**Parameters:**
- `name` (str): Name for this snapshot (default: "default")
- `metadata` (dict): Optional metadata to store with snapshot

**Returns:**
- Dictionary containing snapshot data

**Example:**
```python
snapshot = snapenv.capture("my-project", metadata={"author": "Alice"})
```

### `restore(name: str = "default", dry_run: bool = False) -> None`

Restore environment from a previously captured snapshot.

**Parameters:**
- `name` (str): Name of snapshot to restore (default: "default")
- `dry_run` (bool): If True, show what would be installed without installing

**Example:**
```python
# Preview what would be installed
snapenv.restore("my-project", dry_run=True)

# Actually restore
snapenv.restore("my-project")
```

### `embed(name: str = "default", notebook_path: str = None) -> None`

Embed snapshot into Jupyter notebook metadata.

**Parameters:**
- `name` (str): Name of snapshot to embed (default: "default")
- `notebook_path` (str): Path to notebook file (optional, auto-detected in some environments)

**Example:**
```python
snapenv.embed("v1", "analysis.ipynb")
```

### `restore_from_nb(notebook_path: str = None, dry_run: bool = False) -> None`

Restore environment from notebook-embedded snapshot.

**Parameters:**
- `notebook_path` (str): Path to notebook file (optional, auto-detected in some environments)
- `dry_run` (bool): If True, show what would be installed without installing

**Example:**
```python
snapenv.restore_from_nb("shared_analysis.ipynb")
```

## What Gets Captured?

Each snapshot includes:

- **Python version** - Major, minor, and patch version
- **Platform information** - OS, release, and machine architecture
- **All installed packages** - With exact version numbers
- **Colab detection** - Whether running in Google Colab
- **Timestamp** - When snapshot was created
- **Custom metadata** - Any additional information you provide

## Use Cases

### 1. Reproducible Research

```python
# At the start of your research
import snapenv
snapenv.capture("paper-v1")

# ... months of analysis ...

# Before submission, embed in your analysis notebook
snapenv.embed("paper-v1", "analysis.ipynb")
```

### 2. Teaching & Tutorials

```python
# Create a tutorial notebook with specific package versions
snapenv.capture("tutorial-2024")
snapenv.embed("tutorial-2024", "lesson.ipynb")

# Students can restore the exact environment
snapenv.restore_from_nb("lesson.ipynb")
```

### 3. Team Collaboration

```python
# Team member A captures their working environment
snapenv.capture("project-stable")
snapshot = snapenv.capture("project-stable")

# Share the snapshot dict via git, email, etc.
# Team member B restores it
snapenv.restore_from_dict(snapshot)
```

### 4. Environment Debugging

```python
# When something works on one machine but not another
snapenv.capture("working-config")

# On the broken machine, compare:
snapenv.restore("working-config", dry_run=True)
```

## Advanced Usage

### Preview Changes (Dry Run)

```python
# See what would be installed without actually installing
snapenv.restore("my-project", dry_run=True)
```

### Multiple Snapshots

```python
# Capture different configurations
snapenv.capture("dev")
snapenv.capture("production")
snapenv.capture("minimal")

# Switch between them
snapenv.restore("production")
```

### Working with Snapshot Data

```python
# Get the snapshot dictionary
snapshot = snapenv.capture("test")

# Access snapshot details
print(f"Python version: {snapshot['python_version']}")
print(f"Package count: {len(snapshot['packages'])}")
print(f"Created: {snapshot['timestamp']}")

# Save to file
import json
with open("snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

# Restore from file later
with open("snapshot.json", "r") as f:
    loaded = json.load(f)
snapenv.restore_from_dict(loaded)
```

## Error Handling

`snapenv` provides informative error messages and graceful degradation:

```python
try:
    snapenv.restore("my-project")
except snapenv.RestoreError as e:
    print(f"Restoration failed: {e}")
```

**Common scenarios:**
- Python version mismatches → Warning issued, continues with installation
- Package installation failures → Individual packages skipped with warnings
- Missing snapshots → Clear error message with available snapshot names

## Limitations

- **Package sources**: Only captures pip-installed packages (not conda, system packages, etc.)
- **Binary dependencies**: Cannot capture system libraries or non-Python dependencies
- **Platform differences**: Snapshots capture platform info but cannot enforce it
- **Version conflicts**: Some package combinations may be impossible to install together

## Development

### Setup Development Environment

```bash
git clone https://github.com/lovnishverma/snapenv.git
cd snapenv
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
pytest --cov=snapenv --cov-report=html
```

### Code Quality

```bash
black snapenv tests
ruff check snapenv tests
mypy snapenv
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the test suite
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## FAQ

**Q: Does this work outside of Jupyter/Colab?**  
A: Yes! The core capture/restore functionality works in any Python environment. The notebook features require Jupyter.

**Q: Can I use this in production applications?**  
A: `snapenv` is designed for notebooks and development workflows. For production, consider Docker, conda environments, or proper dependency management tools.

**Q: What if a package version isn't available anymore?**  
A: `snapenv` will warn you and skip that package, installing everything else that's available.

**Q: Does this capture virtual environment state?**  
A: No, it captures installed packages regardless of whether you're in a venv. It's meant for recreating package sets, not virtual environment structure.

**Q: How is this different from `pip freeze`?**  
A: `snapenv` adds platform/Python version tracking, Jupyter integration, user-friendly interfaces, and graceful error handling. It's specifically designed for notebook reproducibility.

## Changelog

### v0.1.0 (2024)
- Initial release
- Core capture/restore functionality
- Notebook metadata embedding
- Google Colab support
- Comprehensive test suite

## Support

- 📧 **Issues**: [GitHub Issues](https://github.com/lovnishverma/snapenv/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/lovnishverma/snapenv/discussions)
- 📖 **Documentation**: [README](https://github.com/lovnishverma/snapenv#readme)

---

Made with ❤️ for the Jupyter and Google Colab community