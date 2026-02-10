#!/usr/bin/env python3
"""
Verify snapenv package structure and functionality.
Run this before building/publishing.
"""

import sys
import os
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} MISSING: {path}")
        return False


def verify_package_structure():
    """Verify the package has correct structure."""
    print("=" * 60)
    print("PACKAGE STRUCTURE VERIFICATION")
    print("=" * 60)
    
    root = Path(__file__).parent
    all_good = True
    
    # Core files
    all_good &= check_file_exists(root / "pyproject.toml", "Build config")
    all_good &= check_file_exists(root / "README.md", "README")
    all_good &= check_file_exists(root / "LICENSE", "License")
    
    # Package files
    pkg_root = root / "snapenv"
    all_good &= check_file_exists(pkg_root / "__init__.py", "Package init")
    all_good &= check_file_exists(pkg_root / "__version__.py", "Version")
    all_good &= check_file_exists(pkg_root / "models.py", "Models")
    all_good &= check_file_exists(pkg_root / "capture.py", "Capture")
    all_good &= check_file_exists(pkg_root / "restore.py", "Restore")
    all_good &= check_file_exists(pkg_root / "colab.py", "Colab utils")
    all_good &= check_file_exists(pkg_root / "notebook.py", "Notebook")
    all_good &= check_file_exists(pkg_root / "exceptions.py", "Exceptions")
    
    # Test files
    test_root = root / "tests"
    all_good &= check_file_exists(test_root / "__init__.py", "Tests init")
    
    print()
    return all_good


def verify_imports():
    """Verify package can be imported."""
    print("=" * 60)
    print("IMPORT VERIFICATION")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        
        print("Importing snapenv...", end=" ")
        import snapenv
        print("✓")
        
        print(f"Version: {snapenv.__version__}")
        
        # Check public API
        api_functions = ["capture", "restore", "embed", "restore_from_nb"]
        for func_name in api_functions:
            if hasattr(snapenv, func_name):
                print(f"✓ API function: {func_name}")
            else:
                print(f"✗ MISSING API function: {func_name}")
                return False
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def main():
    """Run all verifications."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "SNAPENV VERIFICATION" + " " * 23 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    results = {
        "Package Structure": verify_package_structure(),
        "Imports": verify_imports(),
    }
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
        all_passed &= passed
    
    print()
    
    if all_passed:
        print("✓ All verifications passed!")
        print()
        print("Next steps:")
        print("  1. Install: pip install -e .")
        print("  2. Test: pytest (if installed)")
        print("  3. Build: python -m build")
        print("  4. Publish: twine upload dist/*")
        return 0
    else:
        print("✗ Some verifications failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
