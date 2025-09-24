"""
Converters for different output formats.

This module provides specialized classes for converting HWPX files to various
output formats like text, markdown, and batch processing capabilities.
"""

import os
import re
import glob
from pathlib import Path
from .core import HWPXProcessor


class TextExtractor:
    """
    Simple text extraction from HWPX files.
    
    This class provides a straightforward interface for extracting plain text
    from HWPX files without additional formatting.
    """
    
    def __init__(self, jar_path=None):
        """
        Initialize the text extractor.
        
        Args:
            jar_path (str, optional): Path to the hwpxlib JAR file
        """
        self.processor = HWPXProcessor(jar_path)
    
    def extract_to_string(self, filepath, insert_para_head=False):
        """
        Extract text from HWPX file to string.
        
        Args:
            filepath (str): Path to the HWPX file
            insert_para_head (bool): Whether to insert paragraph headers
            
        Returns:
            str: Extracted text
        """
        return self.processor.load_file(filepath).extract_text(insert_para_head)
    
    def extract_to_file(self, input_file, output_file, insert_para_head=False):
        """
        Extract text from HWPX file and save to text file.
        
        Args:
            input_file (str): Path to input HWPX file
            output_file (str): Path to output text file
            insert_para_head (bool): Whether to insert paragraph headers
        """
        text = self.extract_to_string(input_file, insert_para_head)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)


class MarkdownFormatter:
    """Helper class to format extracted text as Markdown."""
    
    def __init__(self, format_tables=True, preserve_linebreaks=False):
        """
        Initialize the markdown formatter.
        
        Args:
            format_tables (bool): Whether to format tables as markdown tables
            preserve_linebreaks (bool): Whether to preserve original line breaks
        """
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


class MarkdownConverter:
    """
    Convert HWPX files to Markdown format.
    
    This class provides functionality to convert HWPX files to well-formatted
    Markdown with support for tables and various formatting options.
    """
    
    def __init__(self, jar_path=None, format_tables=True, preserve_linebreaks=False):
        """
        Initialize the markdown converter.
        
        Args:
            jar_path (str, optional): Path to the hwpxlib JAR file
            format_tables (bool): Whether to format tables as markdown tables
            preserve_linebreaks (bool): Whether to preserve original line breaks
        """
        self.processor = HWPXProcessor(jar_path)
        self.formatter = MarkdownFormatter(format_tables, preserve_linebreaks)
    
    def convert_to_string(self, filepath):
        """
        Convert HWPX file to Markdown string.
        
        Args:
            filepath (str): Path to the HWPX file
            
        Returns:
            str: Formatted Markdown text
        """
        text = self.processor.load_file(filepath).extract_text()
        return self.formatter.format_text(text)
    
    def convert_to_file(self, input_file, output_file):
        """
        Convert HWPX file to Markdown file.
        
        Args:
            input_file (str): Path to input HWPX file
            output_file (str): Path to output Markdown file
        """
        markdown = self.convert_to_string(input_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)


class BatchConverter:
    """
    Batch convert multiple HWPX files.
    
    This class provides functionality to convert multiple HWPX files in batch,
    with support for directory traversal and various output formats.
    """
    
    def __init__(self, jar_path=None):
        """
        Initialize the batch converter.
        
        Args:
            jar_path (str, optional): Path to the hwpxlib JAR file
        """
        self.jar_path = jar_path
    
    def convert_directory(self, input_dir, output_dir, output_format='markdown', 
                         recursive=False, overwrite=False):
        """
        Convert all HWPX files in a directory.
        
        Args:
            input_dir (str): Input directory path
            output_dir (str): Output directory path
            output_format (str): Output format ('text' or 'markdown')
            recursive (bool): Whether to search recursively
            overwrite (bool): Whether to overwrite existing files
            
        Returns:
            tuple: (success_count, total_count)
        """
        # Find all HWPX files
        pattern = "**/*.hwpx" if recursive else "*.hwpx"
        search_path = os.path.join(input_dir, pattern)
        hwpx_files = glob.glob(search_path, recursive=recursive)
        
        if not hwpx_files:
            return 0, 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        extension = '.md' if output_format == 'markdown' else '.txt'
        
        # Create appropriate converter
        if output_format == 'markdown':
            converter = MarkdownConverter(self.jar_path)
        else:
            converter = TextExtractor(self.jar_path)
        
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
                    continue
                
                # Convert the file
                if output_format == 'markdown':
                    converter.convert_to_file(input_file, str(output_path))
                else:
                    converter.extract_to_file(input_file, str(output_path))
                
                success_count += 1
                
            except Exception as e:
                print(f"Error converting {input_file}: {e}")
        
        return success_count, len(hwpx_files)