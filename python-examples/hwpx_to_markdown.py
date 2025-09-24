#!/usr/bin/env python3
"""
HWPX to Markdown Conversion Script

This script converts HWPX files to Markdown format with proper formatting, 
including paragraphs, tables, and other structured elements.

Usage:
    python hwpx_to_markdown.py input.hwpx output.md [--format-tables] [--preserve-linebreaks]

Author: Generated for hwpxlib project
License: Apache-2.0
"""

import sys
import os
import argparse
import re
import jpype
import jpype.imports
from jpype.types import *


class MarkdownFormatter:
    """Helper class to format extracted text as Markdown."""
    
    def __init__(self, format_tables=True, preserve_linebreaks=False):
        self.format_tables = format_tables
        self.preserve_linebreaks = preserve_linebreaks
    
    def format_text(self, text):
        """
        Format extracted text as Markdown.
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Formatted Markdown text
        """
        if not text:
            return ""
        
        # Start with the raw text
        formatted = text
        
        # Clean up excessive whitespace but preserve intentional formatting
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)  # Max 2 consecutive newlines
        formatted = re.sub(r'[ \t]+$', '', formatted, flags=re.MULTILINE)  # Remove trailing spaces
        
        # Format tables if enabled
        if self.format_tables:
            formatted = self._format_tables(formatted)
        
        # Handle line breaks
        if not self.preserve_linebreaks:
            # Convert single line breaks within paragraphs to spaces
            # but preserve paragraph breaks (double newlines) and table rows
            # Split into lines to process each one
            lines = formatted.split('\n')
            processed_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # If this is a table row (starts with |), keep it as is
                if line.strip().startswith('|'):
                    processed_lines.append(line)
                # If this is an empty line, keep it
                elif not line.strip():
                    processed_lines.append(line)
                # Otherwise, check if we should merge with next line
                else:
                    # Look ahead to see if next line should be merged
                    if (i + 1 < len(lines) and 
                        lines[i + 1].strip() and 
                        not lines[i + 1].strip().startswith('|')):
                        # Merge with next line using a space
                        processed_lines.append(line + ' ' + lines[i + 1].strip())
                        i += 1  # Skip the next line since we merged it
                    else:
                        processed_lines.append(line)
                i += 1
            
            formatted = '\n'.join(processed_lines)
        
        # Clean up any remaining multiple spaces
        formatted = re.sub(r' {2,}', ' ', formatted)
        
        # Ensure the document ends with a single newline
        formatted = formatted.rstrip() + '\n'
        
        return formatted
    
    def _format_tables(self, text):
        """
        Attempt to format table-like content as Markdown tables.
        This is a simple heuristic-based approach.
        """
        lines = text.split('\n')
        formatted_lines = []
        in_table = False
        table_rows = []
        
        for line in lines:
            # Skip empty lines but keep track of them
            if not line.strip():
                if in_table:
                    # End of table on empty line
                    formatted_lines.extend(self._create_markdown_table(table_rows))
                    in_table = False
                    table_rows = []
                formatted_lines.append(line)
                continue
                
            # Detect potential table rows (lines with multiple tab-separated values)
            if '\t' in line and len(line.split('\t')) >= 2:
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(line.split('\t'))
            else:
                # Not a table line
                if in_table:
                    # End of table, format it
                    formatted_lines.extend(self._create_markdown_table(table_rows))
                    in_table = False
                    table_rows = []
                formatted_lines.append(line)
        
        # Handle table at end of document
        if in_table and table_rows:
            formatted_lines.extend(self._create_markdown_table(table_rows))
        
        return '\n'.join(formatted_lines)
    
    def _create_markdown_table(self, rows):
        """Create a Markdown table from rows of data."""
        if not rows:
            return []
        
        # Find the maximum number of columns
        max_cols = max(len(row) for row in rows)
        
        # Pad all rows to have the same number of columns
        normalized_rows = []
        for row in rows:
            normalized_row = row + [''] * (max_cols - len(row))
            # Clean up cell content
            normalized_row = [cell.strip() for cell in normalized_row]
            normalized_rows.append(normalized_row)
        
        if not normalized_rows:
            return []
        
        markdown_lines = []
        
        # Create header row (treat first row as header)
        header = normalized_rows[0]
        markdown_lines.append('| ' + ' | '.join(header) + ' |')
        
        # Create separator row
        separator = '| ' + ' | '.join(['---' for _ in header]) + ' |'
        markdown_lines.append(separator)
        
        # Create data rows
        for row in normalized_rows[1:]:
            markdown_lines.append('| ' + ' | '.join(row) + ' |')
        
        # Add empty line after table
        markdown_lines.append('')
        
        return markdown_lines


def setup_java_environment():
    """Initialize JPype and setup the Java classpath."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
    
    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR file not found: {jar_path}\n"
                              f"Please build the project first with: mvn clean package")
    
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jar_path])
    
    return jar_path


def convert_hwpx_to_markdown(input_file, output_file, format_tables=True, preserve_linebreaks=False):
    """
    Convert HWPX file to Markdown format.
    
    Args:
        input_file (str): Path to input HWPX file
        output_file (str): Path to output Markdown file
        format_tables (bool): Whether to format tables as Markdown tables
        preserve_linebreaks (bool): Whether to preserve original line breaks
    """
    try:
        # Import Java classes
        from kr.dogfoot.hwpxlib.reader import HWPXReader
        from kr.dogfoot.hwpxlib.tool.textextractor import TextExtractor, TextExtractMethod, TextMarks
        
        print(f"Reading HWPX file: {input_file}")
        
        # Read the HWPX file
        hwpx_file = HWPXReader.fromFilepath(input_file)
        
        # Configure text extraction options for Markdown
        text_marks = TextMarks()
        text_marks.lineBreakAnd("\n")
        text_marks.paraSeparatorAnd("\n\n")
        text_marks.tabAnd("\t")
        
        # Configure table-specific formatting
        if format_tables:
            text_marks.tableRowSeparatorAnd("\n")
            text_marks.tableCellSeparatorAnd("\t")
        
        # Extract text with control text appended
        extracted_text = TextExtractor.extract(
            hwpx_file,
            TextExtractMethod.AppendControlTextAfterParagraphText,
            False,  # insertParaHead
            text_marks
        )
        
        # Convert Java string to Python string
        python_text = str(extracted_text)
        
        print(f"Formatting as Markdown...")
        
        # Format as Markdown
        formatter = MarkdownFormatter(format_tables=format_tables, 
                                    preserve_linebreaks=preserve_linebreaks)
        markdown_text = formatter.format_text(python_text)
        
        print(f"Writing Markdown to: {output_file}")
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        print(f"Conversion completed successfully!")
        print(f"Converted {len(extracted_text)} characters to {len(markdown_text)} characters of Markdown")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise


def main():
    """Main function to handle command line arguments and orchestrate conversion."""
    parser = argparse.ArgumentParser(
        description='Convert HWPX files to Markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hwpx_to_markdown.py document.hwpx document.md
  python hwpx_to_markdown.py document.hwpx document.md --format-tables
  python hwpx_to_markdown.py document.hwpx document.md --preserve-linebreaks
        """
    )
    
    parser.add_argument('input_file', help='Input HWPX file path')
    parser.add_argument('output_file', help='Output Markdown file path')
    parser.add_argument('--format-tables', action='store_true', 
                       help='Format tables as Markdown tables (default: True)')
    parser.add_argument('--no-format-tables', dest='format_tables', action='store_false',
                       help='Do not format tables as Markdown tables')
    parser.add_argument('--preserve-linebreaks', action='store_true',
                       help='Preserve original line breaks (default: False)')
    
    parser.set_defaults(format_tables=True)
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file does not exist: {args.input_file}")
        sys.exit(1)
    
    if not args.input_file.lower().endswith('.hwpx'):
        print(f"Warning: Input file does not have .hwpx extension: {args.input_file}")
    
    try:
        # Setup Java environment
        print("Setting up Java environment...")
        jar_path = setup_java_environment()
        print(f"Using JAR: {jar_path}")
        
        # Convert to Markdown
        convert_hwpx_to_markdown(
            args.input_file, 
            args.output_file, 
            format_tables=args.format_tables,
            preserve_linebreaks=args.preserve_linebreaks
        )
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        if jpype.isJVMStarted():
            jpype.shutdownJVM()


if __name__ == "__main__":
    main()