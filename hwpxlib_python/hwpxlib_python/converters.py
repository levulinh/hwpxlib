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


class MarkdownToHWPXConverter:
    """
    Convert Markdown files to HWPX format.
    
    This class provides functionality to convert Markdown text to HWPX files
    with support for headings, formatting, lists, tables, and URLs.
    """
    
    def __init__(self, jar_path=None):
        """
        Initialize the markdown to HWPX converter.
        
        Args:
            jar_path (str, optional): Path to the hwpxlib JAR file
        """
        self.processor = HWPXProcessor(jar_path)
        
        # Import Java classes after JVM is started
        self._import_java_classes()
    
    def _import_java_classes(self):
        """Import required Java classes."""
        from kr.dogfoot.hwpxlib.tool.blankfilemaker import BlankFileMaker
        from kr.dogfoot.hwpxlib.writer import HWPXWriter
        from kr.dogfoot.hwpxlib.object.content.section_xml.paragraph.t import NormalText
        from kr.dogfoot.hwpxlib.object.content.section_xml.paragraph import Para, Run, T
        import java.lang
        
        self.BlankFileMaker = BlankFileMaker
        self.HWPXWriter = HWPXWriter
        self.NormalText = NormalText
        self.Para = Para
        self.Run = Run
        self.T = T
        self.Integer = java.lang.Integer
    
    def convert_to_file(self, markdown_text, output_file):
        """
        Convert Markdown text to HWPX file.
        
        Args:
            markdown_text (str): Markdown content to convert
            output_file (str): Path to output HWPX file
        """
        # Create a blank HWPX file
        hwpx_file = self.BlankFileMaker.make()
        
        # Parse markdown and populate HWPX content
        self._populate_content(hwpx_file, markdown_text)
        
        # Write to file
        self.HWPXWriter.toFilepath(hwpx_file, output_file)
    
    def convert_from_file(self, input_file, output_file):
        """
        Convert Markdown file to HWPX file.
        
        Args:
            input_file (str): Path to input Markdown file
            output_file (str): Path to output HWPX file
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        self.convert_to_file(markdown_text, output_file)
    
    def _populate_content(self, hwpx_file, markdown_text):
        """
        Parse markdown content and populate HWPX file structure.
        
        Args:
            hwpx_file: The HWPX file object to populate
            markdown_text (str): The markdown content to parse
        """
        # Get the first section (created by BlankFileMaker)
        section = hwpx_file.sectionXMLFileList().get(0)
        
        # Remove the default empty paragraph created by BlankFileMaker
        section.removeAllParas()
        
        # Parse markdown content
        blocks = self._parse_markdown_blocks(markdown_text)
        
        # Convert each block to HWPX paragraphs
        for block in blocks:
            self._convert_block_to_paragraph(section, block)
    
    def _parse_markdown_blocks(self, text):
        """
        Parse markdown text into logical blocks.
        
        Returns:
            List of dictionaries with 'type' and 'content' keys
        """
        blocks = []
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Headers
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6 and line[level:level+1] == ' ':
                    blocks.append({
                        'type': 'heading',
                        'level': level,
                        'content': line[level:].strip()
                    })
                    i += 1
                    continue
            
            # Unordered lists
            if re.match(r'^[-*+]\s', line):
                list_items = []
                while i < len(lines) and re.match(r'^[-*+]\s', lines[i]):
                    list_items.append(lines[i][2:].strip())
                    i += 1
                blocks.append({
                    'type': 'unordered_list',
                    'items': list_items
                })
                continue
            
            # Ordered lists
            if re.match(r'^\d+\.\s', line):
                list_items = []
                while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                    list_items.append(re.sub(r'^\d+\.\s', '', lines[i]))
                    i += 1
                blocks.append({
                    'type': 'ordered_list',
                    'items': list_items
                })
                continue
            
            # Tables
            if '|' in line:
                table_rows = []
                while i < len(lines) and lines[i].strip() and '|' in lines[i]:
                    # Skip separator rows (like |---|---|)
                    if not re.match(r'^\s*\|[\s\-|]*\|\s*$', lines[i]):
                        row_cells = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                        table_rows.append(row_cells)
                    i += 1
                if table_rows:
                    blocks.append({
                        'type': 'table',
                        'rows': table_rows
                    })
                continue
            
            # Regular paragraphs
            paragraph_lines = [line]
            i += 1
            
            # Collect continuation lines
            while i < len(lines) and lines[i].strip() and not self._is_block_start(lines[i]):
                paragraph_lines.append(lines[i].rstrip())
                i += 1
            
            blocks.append({
                'type': 'paragraph',
                'content': ' '.join(paragraph_lines)
            })
        
        return blocks
    
    def _is_block_start(self, line):
        """Check if line starts a new markdown block."""
        return (line.startswith('#') or
                re.match(r'^[-*+]\s', line) or
                re.match(r'^\d+\.\s', line) or
                '|' in line)
    
    def _convert_block_to_paragraph(self, section, block):
        """
        Convert a markdown block to HWPX paragraph(s).
        
        Args:
            section: The section to add paragraphs to
            block: Dictionary with block information
        """
        block_type = block['type']
        
        if block_type == 'heading':
            self._create_heading_paragraph(section, block['content'], block['level'])
        elif block_type == 'paragraph':
            self._create_text_paragraph(section, block['content'])
        elif block_type == 'unordered_list':
            for item in block['items']:
                self._create_list_paragraph(section, item, bullet=True)
        elif block_type == 'ordered_list':
            for i, item in enumerate(block['items'], 1):
                self._create_list_paragraph(section, item, bullet=False, number=i)
        elif block_type == 'table':
            self._create_table_paragraphs(section, block['rows'])
    
    def _create_heading_paragraph(self, section, text, level):
        """Create a heading paragraph."""
        para = section.addNewPara()
        para.idAnd(str(hash(text) % 1000000000))
        para.paraPrIDRefAnd("3")
        para.styleIDRefAnd("0")
        para.pageBreakAnd(False)
        para.columnBreakAnd(False)
        para.merged(False)
        
        run = para.addNewRun()
        run.charPrIDRef("0")
        
        t = run.addNewT()
        t.charPrIDRefAnd("0")
        
        # Add heading prefix
        heading_text = '#' * level + ' ' + text
        t.addText(heading_text)
        
        # Create line segments for proper display
        para.createLineSegArray()
        line_seg = para.lineSegArray().addNew()
        line_seg.textposAnd(self.Integer(0))
        line_seg.vertposAnd(self.Integer(0))
        line_seg.vertsizeAnd(self.Integer(1000))
        line_seg.textheightAnd(self.Integer(1000))
        line_seg.baselineAnd(self.Integer(850))
        line_seg.spacingAnd(self.Integer(600))
        line_seg.horzposAnd(self.Integer(0))
        line_seg.horzsizeAnd(self.Integer(42520))
        line_seg.flags(self.Integer(393216))
    
    def _create_text_paragraph(self, section, text):
        """Create a regular text paragraph with inline formatting."""
        para = section.addNewPara()
        para.idAnd(str(hash(text) % 1000000000))
        para.paraPrIDRefAnd("3")
        para.styleIDRefAnd("0")
        para.pageBreakAnd(False)
        para.columnBreakAnd(False)
        para.merged(False)
        
        run = para.addNewRun()
        run.charPrIDRef("0")
        
        # Parse inline formatting and create text runs
        self._create_formatted_text_runs(run, text)
        
        # Create line segments
        para.createLineSegArray()
        line_seg = para.lineSegArray().addNew()
        line_seg.textposAnd(self.Integer(0))
        line_seg.vertposAnd(self.Integer(0))
        line_seg.vertsizeAnd(self.Integer(1000))
        line_seg.textheightAnd(self.Integer(1000))
        line_seg.baselineAnd(self.Integer(850))
        line_seg.spacingAnd(self.Integer(600))
        line_seg.horzposAnd(self.Integer(0))
        line_seg.horzsizeAnd(self.Integer(42520))
        line_seg.flags(self.Integer(393216))
    
    def _create_formatted_text_runs(self, run, text):
        """Create text runs with inline formatting like bold, italic, etc."""
        # For now, create simple text runs
        # TODO: Parse **bold**, *italic*, `code`, [links](urls)
        
        # Simple implementation - split on markdown formatting
        parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))', text)
        
        for part in parts:
            if not part:
                continue
                
            t = run.addNewT()
            t.charPrIDRefAnd("0")
            
            if part.startswith('**') and part.endswith('**'):
                # Bold text - for now just add as regular text with markers
                t.addText(part)
            elif part.startswith('*') and part.endswith('*'):
                # Italic text - for now just add as regular text with markers
                t.addText(part)
            elif part.startswith('`') and part.endswith('`'):
                # Code text - for now just add as regular text with markers
                t.addText(part)
            elif re.match(r'\[[^\]]+\]\([^)]+\)', part):
                # Link - for now just add as regular text
                t.addText(part)
            else:
                # Regular text
                t.addText(part)
    
    def _create_list_paragraph(self, section, text, bullet=True, number=None):
        """Create a list item paragraph."""
        para = section.addNewPara()
        para.idAnd(str(hash(text) % 1000000000))
        para.paraPrIDRefAnd("3")
        para.styleIDRefAnd("0")
        para.pageBreakAnd(False)
        para.columnBreakAnd(False)
        para.merged(False)
        
        run = para.addNewRun()
        run.charPrIDRef("0")
        
        t = run.addNewT()
        t.charPrIDRefAnd("0")
        
        if bullet:
            list_text = "• " + text
        else:
            list_text = f"{number}. {text}"
        
        t.addText(list_text)
        
        # Create line segments
        para.createLineSegArray()
        line_seg = para.lineSegArray().addNew()
        line_seg.textposAnd(self.Integer(0))
        line_seg.vertposAnd(self.Integer(0))
        line_seg.vertsizeAnd(self.Integer(1000))
        line_seg.textheightAnd(self.Integer(1000))
        line_seg.baselineAnd(self.Integer(850))
        line_seg.spacingAnd(self.Integer(600))
        line_seg.horzposAnd(self.Integer(0))
        line_seg.horzsizeAnd(self.Integer(42520))
        line_seg.flags(self.Integer(393216))
    
    def _create_table_paragraphs(self, section, rows):
        """Create table as formatted text paragraphs."""
        # For simplicity, create table as formatted text
        # TODO: Implement proper table objects
        
        for row in rows:
            para = section.addNewPara()
            para.idAnd(str(hash(str(row)) % 1000000000))
            para.paraPrIDRefAnd("3")
            para.styleIDRefAnd("0")
            para.pageBreakAnd(False)
            para.columnBreakAnd(False)
            para.merged(False)
            
            run = para.addNewRun()
            run.charPrIDRef("0")
            
            t = run.addNewT()
            t.charPrIDRefAnd("0")
            
            # Join cells with tab separators
            table_text = " | ".join(row)
            t.addText(table_text)
            
            # Create line segments
            para.createLineSegArray()
            line_seg = para.lineSegArray().addNew()
            line_seg.textposAnd(self.Integer(0))
            line_seg.vertposAnd(self.Integer(0))
            line_seg.vertsizeAnd(self.Integer(1000))
            line_seg.textheightAnd(self.Integer(1000))
            line_seg.baselineAnd(self.Integer(850))
            line_seg.spacingAnd(self.Integer(600))
            line_seg.horzposAnd(self.Integer(0))
            line_seg.horzsizeAnd(self.Integer(42520))
            line_seg.flags(self.Integer(393216))


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