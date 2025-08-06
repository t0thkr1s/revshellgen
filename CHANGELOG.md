# Changelog

All notable changes to RevShellGen will be documented in this file.

## [2.2.0] - 2025-08-06

### 🔒 Security Improvements
- Replaced `os.system()` with `subprocess.run()` for better security and control
- Improved command execution handling with proper exception catching

### 🐛 Bug Fixes
- Fixed version inconsistencies across package files
- Fixed deprecated GitHub Actions workflow (`actions/create-release@v1` → `softprops/action-gh-release@v1`)
- Improved screen clearing using ANSI escape codes for better cross-platform compatibility

### 📦 Package Improvements
- Updated minimum Python version requirement to 3.8
- Deprecated old `setup.py` in favor of modern `pyproject.toml`
- Synchronized standalone script with packaged version

### 🧹 Code Quality
- Removed duplicate code between standalone and package versions
- Better error handling in listener setup

## [2.1.0] - 2025-08-06

### ✨ New Features
- Added AWK reverse shell type
- Added Socat reverse shell type
- Total shell types increased to 13

### 📚 Documentation
- Updated README with new shell types
- Improved installation instructions

## [2.0.0] - 2025-08-06

### ✨ New Features
- Added comprehensive TTY upgrade instructions
- Added option to save TTY instructions to file
- Added clipboard support for TTY commands
- Improved macOS compatibility with proper netcat detection

### 🏗️ Major Changes
- Complete package restructuring for PyPI distribution
- Added GitHub Actions CI/CD pipeline
- Modern Python packaging with `pyproject.toml`

### 🐛 Bug Fixes
- Fixed macOS netcat listener command syntax (Issue #13)
- Fixed invalid escape sequence warnings in ASCII banner

## [1.4] - 2025-08-06

### Previous Releases
See GitHub releases for version history prior to 2.0.0
