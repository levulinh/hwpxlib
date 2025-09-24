# Python Examples and Library for HWPX to Markdown Conversion

This directory now contains both example scripts and a full Python library for HWPX to Markdown conversion using JPype.

## 🎉 New: Python Library Available!

We've created a proper Python library called `hwpxlib-python` that provides a clean, Pythonic API for working with HWPX files.

### Library Installation

```bash
# Install from the hwpxlib_python directory
cd hwpxlib_python
pip install -e .
```

### Library Usage

```python
from hwpxlib_python import TextExtractor, MarkdownConverter, BatchConverter

# Simple text extraction
extractor = TextExtractor()
text = extractor.extract_to_string('document.hwpx')

# Markdown conversion
converter = MarkdownConverter()
markdown = converter.convert_to_string('document.hwpx')

# Batch processing
batch_converter = BatchConverter()
success, total = batch_converter.convert_directory('input/', 'output/')
```

### CLI Commands

The library also provides convenient command-line tools:

```bash
# Extract text
hwpx-extract document.hwpx output.txt

# Convert to markdown
hwpx-markdown document.hwpx output.md

# Batch convert
hwpx-batch input_folder output_folder
```

## Example Scripts (Legacy)

The original example scripts are still available for reference and learning:

- `basic_text_extraction.py` - Simple text extraction script
- `hwpx_to_markdown.py` - Markdown conversion with table formatting
- `batch_conversion.py` - Batch processing script
- `demo.py` - Comprehensive demonstration
- `setup.py` - Environment setup script

## Which Should You Use?

- **For production use**: Use the `hwpxlib-python` library - it's cleaner, more maintainable, and easier to integrate
- **For learning/examples**: The example scripts are still useful to understand how JPype integration works
- **For quick tasks**: Both work fine, but the CLI tools from the library are more convenient

## Migration Guide

If you've been using the example scripts, here's how to migrate to the library:

**Old way:**
```python
from basic_text_extraction import extract_text_from_hwpx
text = extract_text_from_hwpx('file.hwpx', 'output.txt')
```

**New way:**
```python
from hwpxlib_python import TextExtractor
extractor = TextExtractor()
extractor.extract_to_file('file.hwpx', 'output.txt')
# or just get the string
text = extractor.extract_to_string('file.hwpx')
```

## Prerequisites

1. **Java Development Kit (JDK)**: Java 7 or later
2. **Python**: Python 3.6 or later
3. **Maven**: To build the Java library

## Quick Setup

For a guided setup process, you can use the setup script:

```bash
python setup.py --install-deps
```

This will:
1. Check if Java and Maven are installed
2. Build the Java library automatically  
3. Install Python dependencies
4. Verify everything is working

## Manual Setup

### Step 1: Build the Java library

```bash
cd ..  # Go to project root (where pom.xml is located)
mvn clean package
```

This will create the JAR file at `target/hwpxlib-1.0.7.jar`.

### Step 2: Install Python dependencies

**Option 1: Using pip**
```bash
pip install -r requirements.txt
```

**Option 2: Using uv (if you have it)**
```bash
uv pip install -r requirements.txt
```

**Note**: The main dependency is `JPype1` which requires Java to be installed on your system.

### Step 3: Verify the setup

Run the demo script to verify everything is working:
```bash
python demo.py
```

If you see any errors about missing dependencies or JAR files, the demo script will provide specific instructions on how to fix them.

## Troubleshooting

### macOS JVM Detection Issues

On macOS, you might encounter an error like:
```
Error: [Errno 2] JVM DLL not found: /Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home
```

This happens when JPype finds the browser plugin JVM instead of the actual JDK. To fix this:

1. **Set JAVA_HOME environment variable:**
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home)
   ```

2. **Add it to your shell profile** (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify JAVA_HOME is set correctly:**
   ```bash
   echo $JAVA_HOME
   java -version
   ```

4. **Run the setup script to verify:**
   ```bash
   python setup.py
   ```

### Other Common Issues

- **JPype1 not installed**: Run `pip install JPype1`
- **JAR file not found**: Run `mvn clean package` in the project root
- **Permission errors**: Make sure you have write permissions in the output directories

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