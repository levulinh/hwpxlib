"""
Basic usage examples for hwpxlib-python library.

This script demonstrates the most common use cases for the library.
"""

from hwpxlib_python import HWPXProcessor, TextExtractor, MarkdownConverter, BatchConverter


def example_1_basic_text_extraction():
    """Example 1: Basic text extraction"""
    print("=== Example 1: Basic Text Extraction ===")
    
    try:
        # Simple text extraction
        extractor = TextExtractor()
        text = extractor.extract_to_string('../python-examples/examples/sample_document.hwpx')
        
        print(f"Extracted text (first 200 chars):")
        print(text[:200] + "..." if len(text) > 200 else text)
        
        # Save to file
        extractor.extract_to_file(
            '../python-examples/examples/sample_document.hwpx', 
            'extracted_text.txt'
        )
        print("Text saved to: extracted_text.txt")
        
    except Exception as e:
        print(f"Error: {e}")


def example_2_markdown_conversion():
    """Example 2: Markdown conversion with table formatting"""
    print("\n=== Example 2: Markdown Conversion ===")
    
    try:
        # Convert with table formatting
        converter = MarkdownConverter(format_tables=True)
        markdown = converter.convert_to_string('../python-examples/examples/table_document.hwpx')
        
        print("Converted Markdown:")
        print(markdown)
        
        # Save to file
        converter.convert_to_file(
            '../python-examples/examples/table_document.hwpx',
            'converted_table.md'
        )
        print("Markdown saved to: converted_table.md")
        
    except Exception as e:
        print(f"Error: {e}")


def example_3_core_processor():
    """Example 3: Using the core processor directly"""
    print("\n=== Example 3: Core Processor ===")
    
    try:
        # Create processor and load file
        processor = HWPXProcessor()
        processor.load_file('../python-examples/examples/sample_document.hwpx')
        
        # Extract text with custom settings
        text = processor.extract_text(insert_para_head=True)
        
        print(f"Text extracted using core processor:")
        print(f"File loaded: {processor.is_loaded()}")
        print(f"Text length: {len(text)} characters")
        
    except Exception as e:
        print(f"Error: {e}")


def example_4_batch_conversion():
    """Example 4: Batch conversion"""
    print("\n=== Example 4: Batch Conversion ===")
    
    try:
        # Batch convert all HWPX files in a directory
        batch_converter = BatchConverter()
        success, total = batch_converter.convert_directory(
            '../python-examples/examples',  # input directory
            'batch_output',                  # output directory
            output_format='markdown',
            recursive=False,
            overwrite=True
        )
        
        print(f"Batch conversion completed:")
        print(f"  Successful: {success}/{total}")
        print(f"  Check 'batch_output' directory for results")
        
    except Exception as e:
        print(f"Error: {e}")


def example_5_error_handling():
    """Example 5: Proper error handling"""
    print("\n=== Example 5: Error Handling ===")
    
    # Example of handling non-existent file
    try:
        processor = HWPXProcessor()
        processor.load_file('non_existent_file.hwpx')
    except FileNotFoundError as e:
        print(f"Expected error for missing file: {e}")
    
    # Example of handling unloaded processor
    try:
        processor = HWPXProcessor()
        text = processor.extract_text()  # No file loaded
    except RuntimeError as e:
        print(f"Expected error for unloaded processor: {e}")


if __name__ == "__main__":
    print("HWPX Python Library - Usage Examples")
    print("=" * 50)
    
    # Run all examples
    example_1_basic_text_extraction()
    example_2_markdown_conversion()
    example_3_core_processor()
    example_4_batch_conversion()
    example_5_error_handling()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("Check the generated files:")
    print("- extracted_text.txt")
    print("- converted_table.md")
    print("- batch_output/ directory")