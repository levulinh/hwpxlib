# Python Examples for HWPX to Markdown Conversion

This directory contains Python sample scripts that demonstrate how to convert HWPX files to Markdown format using JPype to run the Java hwpxlib within Python.

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