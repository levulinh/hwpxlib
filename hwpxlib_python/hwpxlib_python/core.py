"""
Core HWPX processing functionality.

This module provides the main HWPXProcessor class that serves as the primary
interface for working with HWPX files.
"""

import os
from .utils import setup_java_environment
import jpype
import jpype.imports


class HWPXProcessor:
    """
    Main processor for HWPX files.
    
    This class provides a convenient interface for loading and processing HWPX files
    using the underlying Java hwpxlib library.
    """
    
    def __init__(self, jar_path=None):
        """
        Initialize the HWPX processor.
        
        Args:
            jar_path (str, optional): Path to the hwpxlib JAR file. If None, will auto-detect.
        """
        self.jar_path = setup_java_environment(jar_path)
        self._hwpx_file = None
        
        # Import Java classes after JVM is started
        self._import_java_classes()
    
    def _import_java_classes(self):
        """Import required Java classes."""
        from kr.dogfoot.hwpxlib.reader import HWPXReader
        from kr.dogfoot.hwpxlib.tool.textextractor import TextExtractor, TextExtractMethod, TextMarks
        
        self.HWPXReader = HWPXReader
        self.TextExtractor = TextExtractor
        self.TextExtractMethod = TextExtractMethod
        self.TextMarks = TextMarks
    
    def load_file(self, filepath):
        """
        Load an HWPX file.
        
        Args:
            filepath (str): Path to the HWPX file to load
            
        Returns:
            HWPXProcessor: Self for method chaining
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If the file cannot be loaded
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"HWPX file not found: {filepath}")
        
        try:
            self._hwpx_file = self.HWPXReader.fromFilepath(filepath)
            return self
        except Exception as e:
            raise Exception(f"Failed to load HWPX file: {e}")
    
    def extract_text(self, insert_para_head=False, text_marks=None):
        """
        Extract plain text from the loaded HWPX file.
        
        Args:
            insert_para_head (bool): Whether to insert paragraph headers
            text_marks (TextMarks, optional): Custom text formatting marks
            
        Returns:
            str: Extracted text
            
        Raises:
            RuntimeError: If no file is loaded
        """
        if not self._hwpx_file:
            raise RuntimeError("No HWPX file loaded. Call load_file() first.")
        
        if text_marks is None:
            text_marks = self.TextMarks()
            text_marks.lineBreakAnd("\n")
            text_marks.paraSeparatorAnd("\n\n")
            text_marks.tabAnd("\t")
            text_marks.tableRowSeparatorAnd("\n")
            text_marks.tableCellSeparatorAnd("\t")
        
        try:
            extracted_text = self.TextExtractor.extract(
                self._hwpx_file,
                self.TextExtractMethod.AppendControlTextAfterParagraphText,
                insert_para_head,
                text_marks
            )
            return str(extracted_text)
        except Exception as e:
            raise Exception(f"Failed to extract text: {e}")
    
    def is_loaded(self):
        """
        Check if an HWPX file is currently loaded.
        
        Returns:
            bool: True if a file is loaded, False otherwise
        """
        return self._hwpx_file is not None
    
    def get_java_object(self):
        """
        Get the underlying Java HWPXFile object.
        
        Returns:
            HWPXFile: The Java object, or None if no file is loaded
        """
        return self._hwpx_file