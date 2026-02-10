# snapmyenv 📸

**Snapshot and restore Python environments for reproducible notebooks.**

`snapmyenv` is a lightweight, zero-dependency library designed to solve the "it works on my machine" problem for **Google Colab** and **Jupyter Notebooks**. It captures your runtime environment—including Python version, OS details, and exact package versions—and embeds it directly into your notebook's metadata.

Share your notebooks with confidence, knowing others can instantly recreate your exact setup with a single command.

[![PyPI version](https://img.shields.io/pypi/v/snapmyenv.svg)](https://pypi.org/project/snapmyenv/)
[![Python Versions](https://img.shields.io/pypi/pyversions/snapmyenv.svg)](https://pypi.org/project/snapmyenv/)
[![License](https://img.shields.io/pypi/l/snapmyenv.svg)](https://github.com/lovnishverma/snapmyenv/blob/main/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🚀 Key Features

- **📸 Full Environment Capture**: Records Python version, OS/Platform, and all installed `pip` packages.
- **📓 Notebook Embedding**: Injects dependency snapshots directly into `.ipynb` metadata—making the notebook a self-contained unit.
- **🌐 Colab Ready**: Includes specific logic to detect and handle Google Colab environments.
- **🛡️ Zero Dependencies**: Built using only the Python standard library (`sys`, `json`, `subprocess`), so installing it never conflicts with your existing environment.
- **🔄 Instant Restore**: Reinstall the exact package versions required to run a notebook with a single function call.
- **⛑️ Safety First**: Includes `dry_run` modes to preview changes before installation.

---

## 📦 Installation

```bash
!pip install snapmyenv

```

---

## ⚡ Quick Start

### 1. The "Self-Reproducible" Notebook (Recommended)

The most powerful way to use `snapmyenv` is to embed the environment *inside* the notebook itself.

**User A (The Author):**

```python
import snapmyenv

# 1. Capture the current environment
snapmyenv.capture("stable-v1")

# 2. Embed it into the notebook metadata
snapmyenv.embed("stable-v1", "my_analysis.ipynb")
# Output: ✓ Embedded snapshot 'stable-v1' into my_analysis.ipynb

```

**User B (The Recipient):**

```python
import snapmyenv

# Restore the exact environment embedded in the file
snapmyenv.restore_from_nb("my_analysis.ipynb")
# Output:
# Found embedded snapshot in my_analysis.ipynb
# Installing packages...
# ✓ Restoration complete.

```

---

## 🎓 Google Colab Guide

Using `snapmyenv` in Google Colab requires one extra step: **mounting Google Drive**. Since Colab instances are temporary, you must save the notebook to your Drive to persist the embedded environment snapshot.

### Step 1: Install & Mount Drive

Run this at the top of your notebook to install the library and give it access to save the file.

```python
!pip install snapmyenv

from google.colab import drive
import snapmyenv

# Mount Google Drive so we can save the notebook file
drive.mount('/content/drive')

```

### Step 2: Capture & Embed

Once your analysis is working perfectly, capture the environment and embed it into the notebook file sitting on your Drive.

```python
# 1. Capture the current Colab environment
snapmyenv.capture("final-submission")

# 2. Embed it into your notebook file (adjust the path to match your file)
notebook_path = "/content/drive/MyDrive/Colab Notebooks/my_analysis.ipynb"
snapmyenv.embed("final-submission", notebook_path)

print("✅ Environment saved! You can now share this notebook.")

```

### Step 3: Restoring (For Others)

When someone else opens your notebook, they can restore your exact environment—even if Colab has updated its default packages since you wrote the code.

```python
!pip install snapmyenv
import snapmyenv
from google.colab import drive
drive.mount('/content/drive')

# Restore the environment from the notebook itself
snapmyenv.restore_from_nb("/content/drive/MyDrive/Colab Notebooks/my_analysis.ipynb")

```

---

## 📖 API Reference

### `capture(name="default", metadata=None) -> dict`

Captures the current Python environment state in memory.

* **name** (`str`): Unique identifier for the snapshot.
* **metadata** (`dict`): Optional dictionary of extra info (e.g., `{'author': 'Jane', 'experiment': '42'}`).
* **Returns**: A dictionary containing the snapshot data.

### `embed(name="default", notebook_path=None) -> None`

Writes a captured snapshot into the JSON metadata of a `.ipynb` file.

* **name** (`str`): Name of the snapshot to embed.
* **notebook_path** (`str`): Path to the notebook. If running in Jupyter, it attempts to auto-detect the path.

### `restore(name="default", dry_run=False) -> None`

Restores an environment from a snapshot currently held in memory.

* **name** (`str`): Name of the snapshot to restore.
* **dry_run** (`bool`): If `True`, prints the list of packages that *would* be installed without actually installing them.

### `restore_from_nb(notebook_path=None, dry_run=False) -> None`

Reads a snapshot *from* a notebook file's metadata and restores it.

* **notebook_path** (`str`): Path to the notebook file.
* **dry_run** (`bool`): Preview changes without installing.

---

## 🔍 What Actually Gets Captured?

Unlike `pip freeze`, `snapmyenv` captures the full context required for debugging environment issues:

| Data Point | Description |
| --- | --- |
| **Python Version** | e.g., `3.10.12` (Major.Minor.Patch) |
| **Platform** | e.g., `Linux-5.15.0-generic` |
| **Architecture** | e.g., `x86_64` |
| **Packages** | Complete list of `pip` packages with pinned versions |
| **Colab Flag** | Boolean flag indicating if the snapshot originated in Colab |
| **Timestamp** | UTC timestamp of capture |

---

## 🛠️ Advanced Usage

### Dry Run (Preview Changes)

Before modifying your environment, see exactly what will change:

```python
snapmyenv.restore_from_nb("analysis.ipynb", dry_run=True)
# Output:
# [DRY RUN] Would install:
#   numpy==1.24.3
#   pandas==2.0.1

```

### Save/Load Snapshots to JSON

If you prefer file-based management over notebook embedding:

```python
import json
import snapmyenv

# Save to JSON
snapshot = snapmyenv.capture("production")
with open("env_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

# Load from JSON
with open("env_snapshot.json", "r") as f:
    data = json.load(f)
snapmyenv.restore_from_dict(data)

```

---

## 💻 Development

### Setup

Clone the repository and install it in editable mode with development dependencies:

```bash
git clone https://github.com/lovnishverma/snapmyenv.git
cd snapmyenv
pip install -e ".[dev]"

```

### Verification Script

The project includes a built-in verification script to check package structure and imports before building. Always run this before submitting a PR:

```bash
python verify_package.py

```

### Testing

Run the comprehensive test suite using `pytest`:

```bash
pytest
# Or with coverage report
pytest --cov=snapmyenv --cov-report=html

```

---

## ⚠️ Limitations

* **Pip Only**: Currently captures standard `pip` packages. Does not support Conda-specific packages or system-level binaries (apt/brew).
* **Virtual Environments**: Captures the *state* of packages (versions), not the virtual environment folder structure itself.
* **Cross-Platform**: While `snapmyenv` records the OS, it cannot guarantee that a package compiled for Linux will have a matching version available for Windows.

---

## 📄 Changelog

### v0.1.4

* Enhanced notebook path detection.
* Improved metadata serialization.
* Added `verify_package.py` for build validation.

### v0.1.0

* Initial release.
* Core capture/restore functionality.
* Google Colab support.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes.
4. Run `python verify_package.py` to ensure integrity.
5. Open a Pull Request.

## 📄 License

MIT License - see [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

Made with ❤️ by Lovnish Verma for the Jupyter and Google Colab community
