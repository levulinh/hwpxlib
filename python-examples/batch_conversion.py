#!/usr/bin/env python3
"""
Batch HWPX to Markdown Conversion Script

This script processes multiple HWPX files in a directory and converts them 
to Markdown format in batch.

Usage:
    python batch_conversion.py input_directory output_directory [options]

Author: Generated for hwpxlib project
License: Apache-2.0
"""

import sys
import os
import argparse
import glob
from pathlib import Path
import jpype
import jpype.imports
from jpype.types import *


def setup_java_environment():
    """Initialize JPype and setup the Java classpath with robust JVM detection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
    
    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR file not found: {jar_path}\n"
                              f"Please build the project first with: mvn clean package")
    
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


def convert_single_file(input_file, output_file, output_format='markdown'):
    """
    Convert a single HWPX file to the specified format.
    
    Args:
        input_file (str): Path to input HWPX file
        output_file (str): Path to output file
        output_format (str): Output format ('text' or 'markdown')
    
    Returns:
        bool: True if conversion succeeded, False otherwise
    """
    try:
        # Import Java classes
        from kr.dogfoot.hwpxlib.reader import HWPXReader
        from kr.dogfoot.hwpxlib.tool.textextractor import TextExtractor, TextExtractMethod, TextMarks
        
        # Read the HWPX file
        hwpx_file = HWPXReader.fromFilepath(input_file)
        
        # Configure text extraction options
        text_marks = TextMarks()
        
        if output_format == 'markdown':
            text_marks.lineBreakAnd("\n")
            text_marks.paraSeparatorAnd("\n\n")
            text_marks.tabAnd("\t")
            text_marks.tableRowSeparatorAnd("\n")
            text_marks.tableCellSeparatorAnd("\t")
        else:  # text format
            text_marks.lineBreakAnd("\n")
            text_marks.paraSeparatorAnd("\n\n")
            text_marks.tabAnd("\t")
        
        # Extract text
        extracted_text = TextExtractor.extract(
            hwpx_file,
            TextExtractMethod.AppendControlTextAfterParagraphText,
            False,  # insertParaHead
            text_marks
        )
        
        # Convert Java string to Python string
        python_text = str(extracted_text)
        
        # Post-process for markdown if needed
        if output_format == 'markdown':
            # Basic markdown formatting
            processed_text = post_process_for_markdown(python_text)
        else:
            processed_text = python_text
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        return True
        
    except Exception as e:
        print(f"Error converting {input_file}: {e}")
        return False


def post_process_for_markdown(text):
    """
    Apply basic markdown post-processing to extracted text.
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Post-processed markdown text
    """
    if not text:
        return ""
    
    import re
    
    # Clean up excessive whitespace
    processed = re.sub(r'\n{3,}', '\n\n', text)
    processed = re.sub(r'[ \t]+$', '', processed, flags=re.MULTILINE)
    
    # Basic table formatting (simple heuristic)
    lines = processed.split('\n')
    result_lines = []
    in_table = False
    table_rows = []
    
    for line in lines:
        # Skip empty lines but preserve them
        if not line.strip():
            if in_table:
                # End table on empty line
                if table_rows:
                    # Add header separator if this looks like a table
                    if len(table_rows) >= 1:
                        result_lines.append(table_rows[0])  # Header row
                        # Add separator
                        cells = table_rows[0].split(' | ')
                        separator = '|' + ''.join([' --- |' for _ in cells])
                        result_lines.append(separator)
                        # Add data rows
                        for row in table_rows[1:]:
                            result_lines.append(row)
                    table_rows = []
                in_table = False
            result_lines.append(line)
            continue
            
        # If line has multiple tab-separated values, format as table row
        if '\t' in line and len(line.split('\t')) >= 2:
            cells = [cell.strip() for cell in line.split('\t')]
            formatted_line = '| ' + ' | '.join(cells) + ' |'
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(formatted_line)
        else:
            # End any current table
            if in_table:
                if table_rows:
                    # Add header separator if this looks like a table
                    if len(table_rows) >= 1:
                        result_lines.append(table_rows[0])  # Header row
                        # Add separator
                        cells_count = table_rows[0].count('|') - 1
                        separator = '|' + ''.join([' --- |' for _ in range(cells_count)])
                        result_lines.append(separator)
                        # Add data rows
                        for row in table_rows[1:]:
                            result_lines.append(row)
                    table_rows = []
                in_table = False
            result_lines.append(line)
    
    # Handle table at end
    if in_table and table_rows:
        if len(table_rows) >= 1:
            result_lines.append(table_rows[0])  # Header row
            # Add separator
            cells_count = table_rows[0].count('|') - 1
            separator = '|' + ''.join([' --- |' for _ in range(cells_count)])
            result_lines.append(separator)
            # Add data rows
            for row in table_rows[1:]:
                result_lines.append(row)
    
    processed = '\n'.join(result_lines)
    
    # Ensure document ends with single newline
    processed = processed.rstrip() + '\n'
    
    return processed


def find_hwpx_files(directory, recursive=False):
    """
    Find all HWPX files in a directory.
    
    Args:
        directory (str): Directory to search in
        recursive (bool): Whether to search recursively
        
    Returns:
        list: List of HWPX file paths
    """
    pattern = "**/*.hwpx" if recursive else "*.hwpx"
    search_path = os.path.join(directory, pattern)
    return glob.glob(search_path, recursive=recursive)


def batch_convert(input_dir, output_dir, output_format='markdown', recursive=False, 
                 overwrite=False):
    """
    Convert all HWPX files in input directory to specified format.
    
    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path
        output_format (str): Output format ('text' or 'markdown')
        recursive (bool): Whether to search input directory recursively
        overwrite (bool): Whether to overwrite existing output files
        
    Returns:
        tuple: (success_count, total_count)
    """
    # Find all HWPX files
    hwpx_files = find_hwpx_files(input_dir, recursive=recursive)
    
    if not hwpx_files:
        print(f"No HWPX files found in {input_dir}")
        return 0, 0
    
    print(f"Found {len(hwpx_files)} HWPX files to convert")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    extension = '.md' if output_format == 'markdown' else '.txt'
    
    for input_file in hwpx_files:
        try:
            # Generate output file path
            input_path = Path(input_file)
            
            if recursive:
                # Preserve directory structure
                rel_path = os.path.relpath(input_file, input_dir)
                output_path = Path(output_dir) / rel_path
                output_path = output_path.with_suffix(extension)
                # Create subdirectories if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                # Flat structure
                output_filename = input_path.stem + extension
                output_path = Path(output_dir) / output_filename
            
            # Check if output file already exists
            if output_path.exists() and not overwrite:
                print(f"Skipping {input_file} - output file exists: {output_path}")
                continue
            
            print(f"Converting: {input_file} -> {output_path}")
            
            # Convert the file
            if convert_single_file(input_file, str(output_path), output_format):
                success_count += 1
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed")
                
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
    
    return success_count, len(hwpx_files)


def main():
    """Main function to handle command line arguments and orchestrate batch conversion."""
    parser = argparse.ArgumentParser(
        description='Batch convert HWPX files to text or markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_conversion.py input_dir output_dir
  python batch_conversion.py input_dir output_dir --format text
  python batch_conversion.py input_dir output_dir --recursive --overwrite
        """
    )
    
    parser.add_argument('input_dir', help='Input directory containing HWPX files')
    parser.add_argument('output_dir', help='Output directory for converted files')
    parser.add_argument('--format', choices=['text', 'markdown'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--recursive', action='store_true',
                       help='Search input directory recursively')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing output files')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory does not exist: {args.input_dir}")
        sys.exit(1)
    
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input path is not a directory: {args.input_dir}")
        sys.exit(1)
    
    try:
        # Setup Java environment
        print("Setting up Java environment...")
        jar_path = setup_java_environment()
        print(f"Using JAR: {jar_path}")
        
        # Perform batch conversion
        success_count, total_count = batch_convert(
            args.input_dir,
            args.output_dir,
            output_format=args.format,
            recursive=args.recursive,
            overwrite=args.overwrite
        )
        
        print(f"\nBatch conversion completed:")
        print(f"  Successful: {success_count}/{total_count}")
        print(f"  Failed: {total_count - success_count}/{total_count}")
        
        if success_count < total_count:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        if jpype.isJVMStarted():
            jpype.shutdownJVM()


if __name__ == "__main__":
    main()