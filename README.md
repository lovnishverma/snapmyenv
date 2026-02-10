# snapmyenv 📸

**Snapshot and restore Python environments for reproducible notebooks**

`snapmyenv` is a lightweight library designed for Google Colab and Jupyter users to capture and restore runtime environments, making notebooks fully reproducible. Share your notebooks with confidence knowing others can recreate your exact environment.

[![PyPI version](https://img.shields.io/pypi/v/snapmyenv.svg)](https://pypi.org/project/snapmyenv/)
[![Python Versions](https://img.shields.io/pypi/pyversions/snapmyenv.svg)](https://pypi.org/project/snapmyenv/)
[![License](https://img.shields.io/pypi/l/snapmyenv.svg)](https://github.com/lovnishverma/snapmyenv/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/snapmyenv)](https://pepy.tech/project/snapmyenv)

## Features

- 📸 **Capture environments** - Snapshot Python version, OS, and all installed packages
- 🔄 **Restore environments** - Recreate exact package versions from snapshots
- 📓 **Notebook integration** - Embed snapshots directly in `.ipynb` metadata
- 🌐 **Colab-friendly** - Designed for Google Colab and local Jupyter
- 🪶 **Zero dependencies** - No external dependencies beyond Python stdlib
- 🛡️ **Production-ready** - Clean error handling, validation, and logging

## Installation

```bash
pip install snapmyenv
```

Based on the files provided, here is an analysis of the **`snapmyenv`** project.

### **Executive Summary**

`snapmyenv` is a lightweight Python library designed to solve the "it works on my machine" problem for **Google Colab** and **Jupyter Notebooks**. It allows users to capture the current state of a Python environment (libraries, versions, OS info) and embed that "snapshot" directly into a notebook's metadata. This makes the notebook self-reproducible, allowing anyone who opens it to restore the exact environment used by the original author.

### **Key Features**

1. **Environment Capture**: It records the Python version, Operating System details (Platform), and a complete list of installed pip packages with their exact versions.
2. **Notebook Embedding**: Unlike `requirements.txt` which is a separate file, `snapmyenv` embeds the dependency snapshot directly into the `.ipynb` file's JSON metadata under the key `snapmyenv_snapshot`.
3. **Restoration**: It can read a snapshot (from memory, a file, or notebook metadata) and reinstall the specific package versions using `pip`.
4. **Colab Integration**: It includes specific utilities to detect if code is running in Google Colab or a standard Jupyter environment.
5. **Zero Dependencies**: The library itself has no external dependencies (only uses the Python standard library), making it easy to install without causing dependency conflicts.

### **Technical Architecture**

* **Data Models (`models.py`)**:
The core data structure is the `EnvironmentSnapshot` dataclass, which holds metadata (timestamp, python version) and a list of `Package` objects. It handles serialization to and from JSON/dict formats.
* **Capture Mechanism (`capture.py`)**:
Instead of relying on `pkg_resources` or `importlib.metadata` directly, it spawns a subprocess running `pip list --format=json`. This is a robust way to get the exact list of installed packages as `pip` sees them.
* **Restore Mechanism (`restore.py`)**:
Restoration involves iterating through the captured package list and calling `pip install package==version` via subprocess. It includes a `dry_run` mode to preview changes without installing them. It also warns the user if the Python version differs from the snapshot.
* **Notebook Integration (`notebook.py`)**:
This module reads the raw JSON of a `.ipynb` file, injects the snapshot dictionary into `metadata["snapmyenv_snapshot"]`, and writes it back to disk. This allows the environment data to travel with the notebook file itself.

### **Code Quality & Best Practices**

* **Modern Packaging**: The project uses `pyproject.toml` for configuration, adhering to modern Python packaging standards (PEP 517/518).
* **Type Hinting**: The code is fully type-hinted, improving readability and allowing for static analysis.
* **Testing**: There is a comprehensive test suite using `pytest` located in the `tests/` directory, covering capture, models, and restoration logic.
* **Safety**: The code includes a verification script (`verify_package.py`) to check structure and imports before distribution.

### **Potential Limitations**

* **Pip Only**: The README explicitly notes it only captures pip-installed packages, not Conda packages or system-level binaries.
* **Virtual Environments**: It captures the *state* of packages, but does not recreate the virtual environment directory structure itself; it simply installs packages into currently active environment.

### **Use Cases**

* **Research Papers**: Researchers can embed the exact environment used to generate their results into the supplementary notebook files.
* **Teaching**: Instructors can distribute problem sets with embedded environments so students don't face version mismatch errors.
* **Debugging**: Developers can capture a "broken" environment state to share with a colleague for troubleshooting.


## Quick Start

### Basic Usage

```python
import snapmyenv

# Capture your current environment
snapshot = snapmyenv.capture("my-analysis")
# ✓ Captured environment 'my-analysis'
#   Python: 3.10.12
#   Platform: Linux
#   Packages: 147
#   Colab: Yes

# Later, restore the exact environment
snapmyenv.restore("my-analysis")
# Installing 147 packages...
# ✓ Restoration complete: 147 succeeded, 0 failed
```

### Make Notebooks Self-Reproducible

Embed your environment snapshot directly into your notebook:

```python
# In your notebook:
import snapmyenv

# 1. Capture environment
snapmyenv.capture("v1")

# 2. Embed in notebook metadata
snapmyenv.embed("v1", "my_analysis.ipynb")
# ✓ Embedded snapshot 'v1' into my_analysis.ipynb

# Now anyone opening your notebook can restore:
snapmyenv.restore_from_nb("my_analysis.ipynb")
```

## Google Colab Example

Perfect for sharing reproducible analyses on Colab:

```python
# At the top of your Colab notebook:
!pip install snapmyenv

import snapmyenv

# Capture your carefully crafted environment
snapmyenv.capture("colab-analysis-v1")

# Save it to your notebook
snapmyenv.embed("colab-analysis-v1", "/content/drive/MyDrive/analysis.ipynb")
```

When someone else opens your notebook:

```python
import snapmyenv

# Restore the exact environment
snapmyenv.restore_from_nb("/content/drive/MyDrive/analysis.ipynb")
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
snapshot = snapmyenv.capture("my-project", metadata={"author": "Alice"})
```

### `restore(name: str = "default", dry_run: bool = False) -> None`

Restore environment from a previously captured snapshot.

**Parameters:**
- `name` (str): Name of snapshot to restore (default: "default")
- `dry_run` (bool): If True, show what would be installed without installing

**Example:**
```python
# Preview what would be installed
snapmyenv.restore("my-project", dry_run=True)

# Actually restore
snapmyenv.restore("my-project")
```

### `embed(name: str = "default", notebook_path: str = None) -> None`

Embed snapshot into Jupyter notebook metadata.

**Parameters:**
- `name` (str): Name of snapshot to embed (default: "default")
- `notebook_path` (str): Path to notebook file (optional, auto-detected in some environments)

**Example:**
```python
snapmyenv.embed("v1", "analysis.ipynb")
```

### `restore_from_nb(notebook_path: str = None, dry_run: bool = False) -> None`

Restore environment from notebook-embedded snapshot.

**Parameters:**
- `notebook_path` (str): Path to notebook file (optional, auto-detected in some environments)
- `dry_run` (bool): If True, show what would be installed without installing

**Example:**
```python
snapmyenv.restore_from_nb("shared_analysis.ipynb")
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
import snapmyenv
snapmyenv.capture("paper-v1")

# ... months of analysis ...

# Before submission, embed in your analysis notebook
snapmyenv.embed("paper-v1", "analysis.ipynb")
```

### 2. Teaching & Tutorials

```python
# Create a tutorial notebook with specific package versions
snapmyenv.capture("tutorial-2024")
snapmyenv.embed("tutorial-2024", "lesson.ipynb")

# Students can restore the exact environment
snapmyenv.restore_from_nb("lesson.ipynb")
```

### 3. Team Collaboration

```python
# Team member A captures their working environment
snapmyenv.capture("project-stable")
snapshot = snapmyenv.capture("project-stable")

# Share the snapshot dict via git, email, etc.
# Team member B restores it
snapmyenv.restore_from_dict(snapshot)
```

### 4. Environment Debugging

```python
# When something works on one machine but not another
snapmyenv.capture("working-config")

# On the broken machine, compare:
snapmyenv.restore("working-config", dry_run=True)
```

## Advanced Usage

### Preview Changes (Dry Run)

```python
# See what would be installed without actually installing
snapmyenv.restore("my-project", dry_run=True)
```

### Multiple Snapshots

```python
# Capture different configurations
snapmyenv.capture("dev")
snapmyenv.capture("production")
snapmyenv.capture("minimal")

# Switch between them
snapmyenv.restore("production")
```

### Working with Snapshot Data

```python
# Get the snapshot dictionary
snapshot = snapmyenv.capture("test")

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
snapmyenv.restore_from_dict(loaded)
```

## Error Handling

`snapmyenv` provides informative error messages and graceful degradation:

```python
try:
    snapmyenv.restore("my-project")
except snapmyenv.RestoreError as e:
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
git clone https://github.com/lovnishverma/snapmyenv.git
cd snapmyenv
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
pytest --cov=snapmyenv --cov-report=html
```

### Code Quality

```bash
black snapmyenv tests
ruff check snapmyenv tests
mypy snapmyenv
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
A: `snapmyenv` is designed for notebooks and development workflows. For production, consider Docker, conda environments, or proper dependency management tools.

**Q: What if a package version isn't available anymore?**  
A: `snapmyenv` will warn you and skip that package, installing everything else that's available.

**Q: Does this capture virtual environment state?**  
A: No, it captures installed packages regardless of whether you're in a venv. It's meant for recreating package sets, not virtual environment structure.

**Q: How is this different from `pip freeze`?**  
A: `snapmyenv` adds platform/Python version tracking, Jupyter integration, user-friendly interfaces, and graceful error handling. It's specifically designed for notebook reproducibility.

## Changelog

### v0.1.0 (2024)
- Initial release
- Core capture/restore functionality
- Notebook metadata embedding
- Google Colab support
- Comprehensive test suite

## Support

- 📧 **Issues**: [GitHub Issues](https://github.com/lovnishverma/snapmyenv/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/lovnishverma/snapmyenv/discussions)
- 📖 **Documentation**: [README](https://github.com/lovnishverma/snapmyenv#readme)

---

Made with ❤️ for the Jupyter and Google Colab community
