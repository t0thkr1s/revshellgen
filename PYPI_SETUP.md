# PyPI Publishing Setup

## One-Time Setup

1. **Create PyPI account**: https://pypi.org/account/register/

2. **Configure Trusted Publisher on PyPI**:
   - Go to: https://pypi.org/manage/account/publishing/
   - Add new publisher:
     - **PyPI Project Name**: `revshellgen`
     - **Owner**: `t0thkr1s`
     - **Repository name**: `revshellgen`
     - **Workflow name**: `python-publish.yml`
     - **Environment**: (leave empty)

## How to Release

1. **Create a GitHub Release**:
   - Go to https://github.com/t0thkr1s/revshellgen/releases
   - Click "Create a new release"
   - Choose a tag (e.g., `v2.0.1`)
   - Fill in release title and notes
   - Click "Publish release"

2. **Automatic Publishing**:
   - GitHub Actions will automatically:
     - Build the package
     - Publish to PyPI
   - Check Actions tab for status

That's it! No API keys, no manual uploads.
