#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    # Remove version constraints for more flexibility
    requirements = [req.split(">=")[0].split("==")[0] for req in requirements]

setup(
    name="revshellgen",
    version="2.0.0",
    author="t0thkr1s",
    author_email="t0thkr1s@icloud.com",
    description="Reverse Shell Generator - Automate reverse shell generation with style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t0thkr1s/revshellgen",
    project_urls={
        "Bug Tracker": "https://github.com/t0thkr1s/revshellgen/issues",
        "Source Code": "https://github.com/t0thkr1s/revshellgen",
    },
    packages=find_packages(),
    package_data={
        'revshellgen': ['commands/*'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "revshellgen=revshellgen.main:main",
        ],
    },
    keywords=[
        "reverse-shell",
        "penetration-testing",
        "security",
        "networking",
        "pentest",
        "redteam",
        "shell",
        "generator",
        "cybersecurity",
        "hacking",
    ],
)
