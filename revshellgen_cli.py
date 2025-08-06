#!/usr/bin/env python3
"""
Wrapper script for backward compatibility.
Users can still run: python3 revshellgen_cli.py
"""

from revshellgen.main import main

if __name__ == "__main__":
    main()
