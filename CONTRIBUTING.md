Here are the `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` files tailored for **snapmyenv**.

I have customized the Contributing guide to match the development workflow found in your `pyproject.toml` and `README.md` (specifically referencing `pytest`, `black`, `ruff`, and your custom `verify_package.py` script).

### 1. CONTRIBUTING.md

Create a file named `CONTRIBUTING.md` in the root of your repository and paste this content:

```markdown
# Contributing to snapmyenv

Thank you for your interest in contributing to `snapmyenv`! We welcome contributions from everyone, whether it's reporting a bug, suggesting a feature, or writing code.

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 How to Contribute

### Reporting Bugs
If you find a bug, please open an issue on GitHub. Include:
- Your operating system and Python version.
- Whether you are running in Google Colab, Jupyter Notebook, or a local script.
- A minimal reproducible example (code snippet).
- The error traceback.

### Suggesting Features
We love new ideas! Please open an issue to discuss your idea before writing code to ensure it aligns with the project's goals.

## 🛠️ Development Setup

1. **Fork and Clone**
   Fork the repository on GitHub, then clone your fork locally:
   ```bash
   git clone [https://github.com/lovnishverma/snapmyenv.git](https://github.com/lovnishverma/snapmyenv.git)
   cd snapmyenv

```

2. **Set Up Environment**
Install the package in editable mode with development dependencies:
```bash
pip install -e ".[dev]"

```


3. **Verify Installation**
Run the built-in verification script to ensure everything is set up correctly:
```bash
python verify_package.py

```



## 🧪 Testing and Linting

We use `pytest` for testing and `black` for code formatting. Please ensure all checks pass before submitting a Pull Request.

### Run Tests

```bash
pytest

```

### Format Code

We use **Black** to ensure consistent code style.

```bash
# Check formatting
black --check .

# Fix formatting automatically
black .

```

### Static Analysis

We use **Ruff** for linting and **Mypy** for type checking.

```bash
ruff check .
mypy .

```

## 📥 Submitting a Pull Request

1. Create a new branch for your feature or fix:
```bash
git checkout -b feature/my-amazing-feature

```


2. Commit your changes with clear, descriptive messages.
3. Push your branch to your fork:
```bash
git push origin feature/my-amazing-feature

```


4. Open a Pull Request (PR) on the main repository.
5. In your PR description, explain what you changed and link to any relevant issues.

## 📋 Release Process (Maintainers Only)

1. Update the version number in `pyproject.toml` and `snapmyenv/__version__.py`.
2. Update `README.md` and `CHANGELOG` if necessary.
3. Run `python verify_package.py` one last time.
4. Build and publish:
```bash
python -m build
twine upload dist/*

```

```
