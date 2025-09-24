#!/usr/bin/env python3
"""
Example: Converting Markdown to HWPX format

This example demonstrates how to use the MarkdownToHWPXConverter to convert
Markdown files to HWPX format with support for various markdown elements.
"""

import sys
import os

# Add the hwpxlib_python to path for this example
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hwpxlib_python.converters import MarkdownToHWPXConverter

def main():
    # Sample markdown content with various elements
    markdown_content = """# Document Title

This is a sample document demonstrating the Markdown to HWPX conversion.

## Text Formatting

Here are examples of **bold text**, *italic text*, and `inline code`.

## Lists

### Bullet Points
- First bullet point
- Second bullet point with **bold text**
- Third bullet point with *italic text*

### Numbered Lists
1. First item
2. Second item
3. Third item with `code`

## Tables

| Product | Price | Stock |
|---------|-------|-------|
| Laptop  | $999  | 15    |
| Mouse   | $25   | 150   |
| Keyboard| $75   | 80    |

## Links

Visit [our website](https://example.com) for more information.

You can also check out [Google](https://google.com).

## Code Examples

Here's some `inline code` within a sentence.

## Multiple Sections

This demonstrates multiple sections and paragraphs working together.

Each paragraph should be properly separated and formatted.

### Subsection

This is a subsection with its own content.

## Conclusion

This document showcases the various markdown features that are supported
by the MarkdownToHWPXConverter class.
"""

    try:
        # Initialize the converter
        # You can specify a custom JAR path if needed
        converter = MarkdownToHWPXConverter()  # Uses auto-detected JAR
        
        # Convert markdown string to HWPX file
        output_path = 'example_output.hwpx'
        converter.convert_to_file(markdown_content, output_path)
        
        print(f"✓ Markdown successfully converted to HWPX format!")
        print(f"✓ Output saved as: {output_path}")
        
        # You can also convert from file to file
        markdown_file = 'sample.md'
        hwpx_file = 'sample.hwpx'
        
        # First create a sample markdown file
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Convert file to file
        converter.convert_from_file(markdown_file, hwpx_file)
        
        print(f"✓ File conversion completed!")
        print(f"✓ {markdown_file} → {hwpx_file}")
        
        # Display file sizes
        print(f"\nFile sizes:")
        print(f"  {markdown_file}: {os.path.getsize(markdown_file)} bytes")
        print(f"  {hwpx_file}: {os.path.getsize(hwpx_file)} bytes")
        
        return True
        
    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)