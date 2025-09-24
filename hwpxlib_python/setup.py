"""
Setup script for hwpxlib-python

A Python library for converting HWPX files to various formats using JPype
to interface with the Java hwpxlib.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['JPype1>=1.4.1']

setup(
    name="hwpxlib-python",
    version="1.0.0",
    author="Generated for hwpxlib project",
    author_email="",
    description="A Python library for converting HWPX files using JPype and hwpxlib",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/levulinh/hwpxlib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov',
            'black',
            'flake8',
        ],
    },
    entry_points={
        'console_scripts': [
            'hwpx-extract=hwpxlib_python.cli:extract_text',
            'hwpx-markdown=hwpxlib_python.cli:convert_markdown',
            'hwpx-batch=hwpxlib_python.cli:batch_convert',
        ],
    },
    include_package_data=True,
    package_data={
        'hwpxlib_python': ['*.md', '*.txt'],
    },
    keywords=['hwpx', 'hancom', 'document', 'conversion', 'markdown', 'text', 'extraction'],
    project_urls={
        'Bug Reports': 'https://github.com/levulinh/hwpxlib/issues',
        'Source': 'https://github.com/levulinh/hwpxlib',
    },
)