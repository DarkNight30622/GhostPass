#!/usr/bin/env python3
"""
GHOST PASS - Privacy-First VPN and IP-Masking Tool
Setup script for package installation
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ghostpass",
    version="1.0.0",
    author="DarkNight",
    author_email="darknight@example.com",
    description="Privacy-first CLI-based VPN and IP-masking tool using TOR network",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DarkNight30622/GhostPass",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "ghostpass=ghostpass.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ghostpass": ["*.yaml", "*.yml", "*.json"],
    },
    keywords="vpn, tor, privacy, security, networking, cli, terminal",
    project_urls={
        "Bug Reports": "https://github.com/DarkNight30622/GhostPass/issues",
        "Source": "https://github.com/DarkNight30622/GhostPass",
        "Documentation": "https://github.com/DarkNight30622/GhostPass#readme",
    },
) 