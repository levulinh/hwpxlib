# HWPX Python Library

A Python library for converting HWPX (Hancom Office) files to various formats using JPype to interface with the Java hwpxlib.

## Features

- **Easy-to-use API**: Clean, Pythonic interface for HWPX file processing
- **Multiple output formats**: Support for plain text and Markdown conversion
- **Table handling**: Intelligent table detection and formatting for Markdown output
- **Batch processing**: Convert multiple files at once with directory traversal
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Command-line tools**: Convenient CLI tools for common tasks

## Installation

### From PyPI (recommended)

```bash
pip install hwpxlib-python
```

### From source

```bash
git clone https://github.com/levulinh/hwpxlib.git
cd hwpxlib/hwpxlib_python
pip install -e .
```

### Prerequisites

1. **Java Development Kit (JDK)**: Java 8 or later
2. **hwpxlib JAR file**: The library will try to auto-detect the JAR file, or you can specify its location

## Quick Start

### Basic Usage

```python
from hwpxlib_python import HWPXProcessor, MarkdownConverter, TextExtractor

# Simple text extraction
extractor = TextExtractor()
text = extractor.extract_to_string('document.hwpx')
print(text)

# Convert to Markdown
converter = MarkdownConverter()
markdown = converter.convert_to_string('document.hwpx')
print(markdown)

# Using the core processor
processor = HWPXProcessor()
processor.load_file('document.hwpx')
text = processor.extract_text()
```

### Advanced Usage

```python
from hwpxlib_python import MarkdownConverter, BatchConverter

# Markdown conversion with options
converter = MarkdownConverter(
    format_tables=True,
    preserve_linebreaks=False
)
converter.convert_to_file('input.hwpx', 'output.md')

# Batch conversion
batch_converter = BatchConverter()
success, total = batch_converter.convert_directory(
    'input_folder',
    'output_folder',
    output_format='markdown',
    recursive=True
)
print(f"Converted {success}/{total} files")
```

## Command Line Interface

The library provides convenient command-line tools:

### Extract text

```bash
hwpx-extract document.hwpx output.txt
hwpx-extract document.hwpx output.txt --para-head
```

### Convert to Markdown

```bash
hwpx-markdown document.hwpx output.md
hwpx-markdown document.hwpx output.md --no-format-tables
```

### Batch conversion

```bash
hwpx-batch input_folder output_folder
hwpx-batch input_folder output_folder --format text --recursive
```

## API Reference

### HWPXProcessor

The core processor class for loading and processing HWPX files.

```python
processor = HWPXProcessor(jar_path=None)
processor.load_file(filepath)
text = processor.extract_text(insert_para_head=False, text_marks=None)
```

### TextExtractor

Simple text extraction functionality.

```python
extractor = TextExtractor(jar_path=None)
text = extractor.extract_to_string(filepath)
extractor.extract_to_file(input_file, output_file)
```

### MarkdownConverter

Convert HWPX files to Markdown format with table support.

```python
converter = MarkdownConverter(
    jar_path=None, 
    format_tables=True, 
    preserve_linebreaks=False
)
markdown = converter.convert_to_string(filepath)
converter.convert_to_file(input_file, output_file)
```

### BatchConverter

Batch convert multiple HWPX files.

```python
converter = BatchConverter(jar_path=None)
success, total = converter.convert_directory(
    input_dir, 
    output_dir, 
    output_format='markdown', 
    recursive=False, 
    overwrite=False
)
```

## Configuration

### JAR Path Detection

The library attempts to locate the hwpxlib JAR file automatically:

1. Checks relative paths from the library installation
2. Looks for `HWPXLIB_JAR_PATH` environment variable
3. You can also pass the path explicitly to any class constructor

### Java Environment

For macOS users who encounter JVM detection issues:

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
```

Add this to your shell profile (`.bashrc`, `.zshrc`, etc.) for persistence.

## Examples

### Converting Korean Documents

```python
from hwpxlib_python import MarkdownConverter

converter = MarkdownConverter(format_tables=True)
converter.convert_to_file('korean_document.hwpx', 'output.md')
```

The library properly handles Korean text encoding and preserves formatting.

### Processing Tables

```python
from hwpxlib_python import MarkdownConverter

# With table formatting
converter = MarkdownConverter(format_tables=True)
markdown = converter.convert_to_string('document_with_tables.hwpx')

# Output will include properly formatted Markdown tables:
# | Name | Score | Grade |
# | --- | --- | --- |
# | Alice | 95 | A |
# | Bob | 87 | B |
```

### Error Handling

```python
from hwpxlib_python import HWPXProcessor

try:
    processor = HWPXProcessor()
    processor.load_file('document.hwpx')
    text = processor.extract_text()
except FileNotFoundError as e:
    print(f"File not found: {e}")
except RuntimeError as e:
    print(f"JVM error: {e}")
except Exception as e:
    print(f"Conversion error: {e}")
```

## Troubleshooting

### Common Issues

1. **JAR file not found**: Ensure the hwpxlib project is built with `mvn clean package`
2. **JVM errors on macOS**: Set `JAVA_HOME` environment variable
3. **Unicode issues**: The library handles Korean text automatically, ensure your output files use UTF-8 encoding

### Getting Help

- Check the [GitHub Issues](https://github.com/levulinh/hwpxlib/issues) for common problems
- Ensure you have the latest version: `pip install --upgrade hwpxlib-python`

## License

Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.