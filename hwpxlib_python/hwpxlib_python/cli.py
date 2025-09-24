"""
Command-line interface for hwpxlib-python.

This module provides command-line scripts that can be used as entry points
when the library is installed.
"""

import argparse
import sys
import os
from .converters import TextExtractor, MarkdownConverter, BatchConverter


def extract_text():
    """Command-line interface for text extraction."""
    parser = argparse.ArgumentParser(
        description='Extract plain text from HWPX files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hwpx-extract document.hwpx output.txt
  hwpx-extract document.hwpx output.txt --para-head
        """
    )
    
    parser.add_argument('input_file', help='Input HWPX file path')
    parser.add_argument('output_file', help='Output text file path')
    parser.add_argument('--para-head', action='store_true',
                       help='Insert paragraph headers')
    parser.add_argument('--jar-path', type=str,
                       help='Path to hwpxlib JAR file (optional)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file does not exist: {args.input_file}")
        sys.exit(1)
    
    try:
        extractor = TextExtractor(args.jar_path)
        extractor.extract_to_file(args.input_file, args.output_file, args.para_head)
        print(f"Text extracted successfully to: {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def convert_markdown():
    """Command-line interface for Markdown conversion."""
    parser = argparse.ArgumentParser(
        description='Convert HWPX files to Markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hwpx-markdown document.hwpx output.md
  hwpx-markdown document.hwpx output.md --no-format-tables
  hwpx-markdown document.hwpx output.md --preserve-linebreaks
        """
    )
    
    parser.add_argument('input_file', help='Input HWPX file path')
    parser.add_argument('output_file', help='Output Markdown file path')
    parser.add_argument('--format-tables', action='store_true', default=True,
                       help='Format tables as Markdown tables (default: True)')
    parser.add_argument('--no-format-tables', dest='format_tables', action='store_false',
                       help='Do not format tables as Markdown tables')
    parser.add_argument('--preserve-linebreaks', action='store_true',
                       help='Preserve original line breaks (default: False)')
    parser.add_argument('--jar-path', type=str,
                       help='Path to hwpxlib JAR file (optional)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file does not exist: {args.input_file}")
        sys.exit(1)
    
    try:
        converter = MarkdownConverter(args.jar_path, args.format_tables, args.preserve_linebreaks)
        converter.convert_to_file(args.input_file, args.output_file)
        print(f"Markdown conversion completed: {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def batch_convert():
    """Command-line interface for batch conversion."""
    parser = argparse.ArgumentParser(
        description='Batch convert HWPX files to text or markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hwpx-batch input_dir output_dir
  hwpx-batch input_dir output_dir --format text
  hwpx-batch input_dir output_dir --recursive --overwrite
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
    parser.add_argument('--jar-path', type=str,
                       help='Path to hwpxlib JAR file (optional)')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory does not exist: {args.input_dir}")
        sys.exit(1)
    
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input path is not a directory: {args.input_dir}")
        sys.exit(1)
    
    try:
        converter = BatchConverter(args.jar_path)
        success_count, total_count = converter.convert_directory(
            args.input_dir,
            args.output_dir,
            output_format=args.format,
            recursive=args.recursive,
            overwrite=args.overwrite
        )
        
        print(f"Batch conversion completed:")
        print(f"  Successful: {success_count}/{total_count}")
        print(f"  Failed: {total_count - success_count}/{total_count}")
        
        if success_count < total_count:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)