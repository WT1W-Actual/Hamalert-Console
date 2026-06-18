#!/usr/bin/env python3
"""
Setup script for HamAlert Client.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="hamalert-client",
    version="0.1.0",
    author="Jim Perry WT1W/FEPLabs Radio",
    author_email="jp@feplabs.com",
    description="A Python client for hamalert.org telnet DX cluster feed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hamalert/client",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    # No third-party dependencies — uses stdlib socket only.
    entry_points={
        'console_scripts': [
            'hamalert=src.main:main',
        ],
    },
)
