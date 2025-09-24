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
    """Initialize JPype and setup the Java classpath with robust JVM detection."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
    
    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR file not found: {jar_path}\n"
                              f"Please build the project first with: mvn clean package")
    
    # Start JVM with the JAR in classpath
    if not jpype.isJVMStarted():
        # Try to find the correct JVM path, especially important on macOS
        jvm_path = None
        
        # First, try to get JAVA_HOME from environment
        java_home = os.environ.get('JAVA_HOME')
        if java_home and os.path.exists(java_home):
            # Look for the JVM library in common locations
            possible_jvm_paths = [
                os.path.join(java_home, 'lib', 'server', 'libjvm.dylib'),  # macOS
                os.path.join(java_home, 'lib', 'server', 'libjvm.so'),     # Linux
                os.path.join(java_home, 'bin', 'server', 'jvm.dll'),       # Windows
                os.path.join(java_home, 'jre', 'lib', 'server', 'libjvm.dylib'),  # macOS older versions
                os.path.join(java_home, 'jre', 'lib', 'server', 'libjvm.so'),     # Linux older versions
            ]
            
            for path in possible_jvm_paths:
                if os.path.exists(path):
                    jvm_path = path
                    break
        
        # If JAVA_HOME didn't work, try to detect using java command
        if not jvm_path:
            try:
                import subprocess
                # Use java -XshowSettings:properties to get java.home
                result = subprocess.run(['java', '-XshowSettings:properties', '-version'], 
                                      capture_output=True, text=True)
                # Java prints properties to stderr, so check both stdout and stderr
                output = result.stderr + result.stdout
                if result.returncode == 0:
                    for line in output.split('\n'):
                        if 'java.home' in line:
                            java_home = line.split('=')[-1].strip()
                            # Look for JVM library
                            possible_jvm_paths = [
                                os.path.join(java_home, 'lib', 'server', 'libjvm.dylib'),  # macOS
                                os.path.join(java_home, 'lib', 'server', 'libjvm.so'),     # Linux
                                os.path.join(java_home, 'bin', 'server', 'jvm.dll'),       # Windows
                            ]
                            
                            for path in possible_jvm_paths:
                                if os.path.exists(path):
                                    jvm_path = path
                                    break
                            break
            except:
                pass  # Fall back to default JPype detection
        
        # Start JVM with explicit path if found, otherwise let JPype auto-detect
        try:
            if jvm_path:
                jpype.startJVM(jvm_path, classpath=[jar_path])
            else:
                jpype.startJVM(classpath=[jar_path])
        except Exception as e:
            # If JPype fails, provide helpful error message
            raise RuntimeError(f"Failed to start JVM: {e}\n"
                             f"This often happens on macOS when the wrong JVM is detected.\n"
                             f"Try setting JAVA_HOME environment variable to your JDK installation.\n"
                             f"For example: export JAVA_HOME=$(/usr/libexec/java_home)")
    
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