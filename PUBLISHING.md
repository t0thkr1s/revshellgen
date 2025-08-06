# Publishing to PyPI

This guide explains how to publish RevShellGen to the Python Package Index (PyPI).

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Install required tools:
   ```bash
   pip install --upgrade pip setuptools wheel twine
   ```

## Building the Package

1. Clean previous builds:
   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

2. Build the distribution packages:
   ```bash
   python3 setup_pypi.py sdist bdist_wheel
   ```

## Testing with TestPyPI (Recommended)

1. Upload to TestPyPI first:
   ```bash
   twine upload --repository testpypi dist/*
   ```

2. Test installation from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ revshellgen
   ```

## Publishing to PyPI

1. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

2. Verify installation:
   ```bash
   pip install revshellgen
   ```

## After Publishing

Users can install RevShellGen with:
```bash
pip install revshellgen
```

And run it with:
```bash
revshellgen
```

## Version Management

To release a new version:
1. Update version in `revshellgen/__init__.py`
2. Update version in `setup_pypi.py`
3. Update version in `pyproject.toml`
4. Commit changes
5. Create a git tag: `git tag v2.0.0`
6. Push tag: `git push origin v2.0.0`
7. Build and publish as described above

## API Token (Recommended)

Instead of using username/password, use API tokens:
1. Generate token at https://pypi.org/manage/account/token/
2. Create `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = your-api-token-here
   ```
