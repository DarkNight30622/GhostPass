"""
Setup script for GHOST PASS

A privacy-first CLI-based VPN and IP-masking tool that routes traffic through TOR.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="ghostpass",
    version="0.1.0",
    author="GHOST PASS Team",
    author_email="team@ghostpass.dev",
    description="Privacy-First CLI-Based VPN & IP-Masking Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostpass/ghostpass",
    project_urls={
        "Bug Tracker": "https://github.com/ghostpass/ghostpass/issues",
        "Documentation": "https://github.com/ghostpass/ghostpass/docs",
        "Source Code": "https://github.com/ghostpass/ghostpass",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
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
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "build": [
            "pyinstaller>=5.13.0",
            "nuitka>=1.8.0",
            "wheel>=0.40.0",
            "setuptools>=65.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ghostpass=ghostpass.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ghostpass": [
            "config/*.yaml",
            "config/*.json",
            "docs/*.md",
        ],
    },
    keywords=[
        "vpn",
        "tor",
        "privacy",
        "security",
        "encryption",
        "proxy",
        "anonymity",
        "network",
        "cli",
        "terminal",
    ],
    platforms=["Windows", "Linux", "macOS"],
    license="MIT",
    zip_safe=False,
) 