#!/usr/bin/env python3
"""
Basic HWPX Text Extraction Script

This script demonstrates how to extract plain text from HWPX files using JPype 
to run the Java hwpxlib within Python.

Usage:
    python basic_text_extraction.py input.hwpx output.txt

Author: Generated for hwpxlib project
License: Apache-2.0
"""

import sys
import os
import jpype
import jpype.imports
from jpype.types import *


def setup_java_environment():
    """Initialize JPype and setup the Java classpath."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
    
    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR file not found: {jar_path}\n"
                              f"Please build the project first with: mvn clean package")
    
    # Start JVM with the JAR in classpath
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jar_path])
    
    return jar_path


def extract_text_from_hwpx(input_file, output_file):
    """
    Extract plain text from HWPX file and save to output file.
    
    Args:
        input_file (str): Path to input HWPX file
        output_file (str): Path to output text file
    """
    try:
        # Import Java classes
        from kr.dogfoot.hwpxlib.reader import HWPXReader
        from kr.dogfoot.hwpxlib.tool.textextractor import TextExtractor, TextExtractMethod, TextMarks
        
        print(f"Reading HWPX file: {input_file}")
        
        # Read the HWPX file
        hwpx_file = HWPXReader.fromFilepath(input_file)
        
        # Configure text extraction options
        text_marks = TextMarks()
        text_marks.lineBreakAnd("\n")
        text_marks.paraSeparatorAnd("\n\n")
        text_marks.tabAnd("\t")
        # Configure table formatting for better structure
        text_marks.tableRowSeparatorAnd("\n")
        text_marks.tableCellSeparatorAnd("\t")
        
        # Extract text
        extracted_text = TextExtractor.extract(
            hwpx_file,
            TextExtractMethod.AppendControlTextAfterParagraphText,
            False,  # insertParaHead
            text_marks
        )
        
        print(f"Writing extracted text to: {output_file}")
        
        # Convert Java string to Python string
        python_text = str(extracted_text)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_text)
        
        print(f"Extraction completed successfully!")
        print(f"Extracted {len(extracted_text)} characters")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        raise


def main():
    """Main function to handle command line arguments and orchestrate extraction."""
    if len(sys.argv) != 3:
        print("Usage: python basic_text_extraction.py input.hwpx output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: Input file does not exist: {input_file}")
        sys.exit(1)
    
    if not input_file.lower().endswith('.hwpx'):
        print(f"Warning: Input file does not have .hwpx extension: {input_file}")
    
    try:
        # Setup Java environment
        print("Setting up Java environment...")
        jar_path = setup_java_environment()
        print(f"Using JAR: {jar_path}")
        
        # Extract text
        extract_text_from_hwpx(input_file, output_file)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        # Shutdown JVM (optional - it will shutdown automatically when Python exits)
        if jpype.isJVMStarted():
            jpype.shutdownJVM()


if __name__ == "__main__":
    main()