# Setting Up PyPI Publishing with GitHub Actions

This guide explains how to configure GitHub Actions to automatically publish to PyPI.

## Prerequisites

1. PyPI account: https://pypi.org/account/register/
2. TestPyPI account: https://test.pypi.org/account/register/

## Setup Steps

### 1. Configure PyPI Trusted Publishing

#### For PyPI (Production):

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new publisher with these settings:
   - **PyPI Project Name**: `revshellgen`
   - **Owner**: `t0thkr1s`
   - **Repository name**: `revshellgen`
   - **Workflow name**: `python-publish.yml`
   - **Environment**: `pypi`

#### For TestPyPI:

1. Go to https://test.pypi.org/manage/account/publishing/
2. Add a new publisher with these settings:
   - **PyPI Project Name**: `revshellgen`
   - **Owner**: `t0thkr1s`
   - **Repository name**: `revshellgen`
   - **Workflow name**: `python-publish.yml`
   - **Environment**: `testpypi`

### 2. Configure GitHub Repository

#### Create Environments:

1. Go to Settings → Environments in your GitHub repository
2. Create two environments:
   - `pypi` (for production releases)
   - `testpypi` (for test releases)

#### Optional: Add Protection Rules:

For the `pypi` environment, you might want to add:
- Required reviewers
- Deployment branches (only from tags)

### 3. How It Works

The workflow is configured to:

1. **On every push to master**: 
   - Run tests
   - Build package
   - Publish to TestPyPI

2. **On version tags (v*.*.*)**: 
   - Run tests
   - Build package
   - Publish to PyPI
   - Create GitHub Release

### 4. Creating a Release

To create a new release:

```bash
# 1. Update version in files (or use the version-bump workflow)
# 2. Commit changes
git add -A
git commit -m "Bump version to 2.0.1"

# 3. Create and push tag
git tag -a v2.0.1 -m "Release version 2.0.1"
git push origin master
git push origin v2.0.1
```

Or use the GitHub Actions UI:
1. Go to Actions → Version Bump
2. Select version type (patch/minor/major)
3. Run workflow

### 5. Manual Publishing

If you need to publish manually:

```bash
# Build
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Troubleshooting

### Common Issues:

1. **"Trusted publishing not configured"**
   - Ensure the workflow name matches exactly
   - Check environment names match

2. **"Package exists"**
   - Version already published
   - Bump version number

3. **"Invalid distribution"**
   - Run `twine check dist/*` locally
   - Ensure all files are included in MANIFEST.in

## Security Notes

- No API tokens needed with trusted publishing!
- GitHub OIDC handles authentication
- More secure than storing tokens as secrets
