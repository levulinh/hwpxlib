"""
HWPX Python Library

A Python library for converting HWPX files to various formats using JPype to interface with the Java hwpxlib.

This library provides a clean, Pythonic interface to the hwpxlib Java library for processing HWPX files.
"""

from .core import HWPXProcessor
from .converters import TextExtractor, MarkdownConverter, MarkdownToHWPXConverter, BatchConverter
from .utils import setup_java_environment

__version__ = "1.0.0"
__author__ = "Generated for hwpxlib project"
__license__ = "Apache-2.0"

__all__ = [
    'HWPXProcessor',
    'TextExtractor', 
    'MarkdownConverter',
    'MarkdownToHWPXConverter',
    'BatchConverter',
    'setup_java_environment'
]