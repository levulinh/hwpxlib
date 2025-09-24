# Python Examples for HWPX to Markdown Conversion

This directory contains Python sample scripts that demonstrate how to convert HWPX files to Markdown format using JPype to run the Java hwpxlib within Python.

## Prerequisites

1. **Java Development Kit (JDK)**: Java 7 or later
2. **Python**: Python 3.6 or later
3. **Maven**: To build the Java library

## Setup

1. **Build the Java library**:
   ```bash
   cd ..  # Go to project root
   mvn clean package
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Scripts

### `basic_text_extraction.py`
Basic script that extracts plain text from HWPX files.

**Usage**:
```bash
python basic_text_extraction.py input.hwpx output.txt
```

### `hwpx_to_markdown.py`
Advanced script that converts HWPX files to Markdown format with proper formatting.

**Usage**:
```bash
python hwpx_to_markdown.py input.hwpx output.md
```

### `batch_conversion.py`
Batch conversion script for processing multiple HWPX files.

**Usage**:
```bash
python batch_conversion.py input_directory output_directory
```

## Configuration

The scripts support various configuration options for customizing the output format:

- **Line breaks**: `\n` or `<br>`
- **Paragraph separators**: `\n\n` or custom separators
- **Table formatting**: Markdown tables or plain text
- **Text formatting**: Preserve bold, italic, etc.

## Examples

See the `examples/` directory for sample HWPX files and their converted outputs.