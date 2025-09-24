#!/usr/bin/env python3
"""
Demo Script for HWPX to Markdown Conversion

This script demonstrates the usage of all the conversion tools with sample files.

Author: Generated for hwpxlib project
License: Apache-2.0
"""

import os
import sys
import subprocess


def run_demo():
    """Run demonstration of all conversion scripts."""
    print("=" * 60)
    print("HWPX to Markdown Conversion Demo")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if JAR exists
    project_root = os.path.dirname(script_dir)
    jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
    
    if not os.path.exists(jar_path):
        print("Error: JAR file not found!")
        print(f"Expected location: {jar_path}")
        print("Please build the project first with: mvn clean package")
        return False
    
    # Check for example files
    sample_file = os.path.join(script_dir, "examples", "sample_document.hwpx")
    table_file = os.path.join(script_dir, "examples", "table_document.hwpx")
    
    if not os.path.exists(sample_file):
        print(f"Error: Sample file not found: {sample_file}")
        return False
    
    print(f"Using JAR: {jar_path}")
    print(f"Sample files found:")
    print(f"  - {sample_file}")
    if os.path.exists(table_file):
        print(f"  - {table_file}")
    print()
    
    # Demo 1: Basic text extraction
    print("1. Basic Text Extraction Demo")
    print("-" * 30)
    cmd = [sys.executable, "basic_text_extraction.py", 
           "examples/sample_document.hwpx", "examples/demo_text_output.txt"]
    
    try:
        result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Basic text extraction completed successfully")
            # Show first few lines of output
            output_file = os.path.join(script_dir, "examples", "demo_text_output.txt")
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:3]
                    print("  First few lines of extracted text:")
                    for line in lines:
                        print(f"    {line.strip()}")
        else:
            print("✗ Basic text extraction failed")
            print(f"  Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Failed to run basic text extraction: {e}")
    
    print()
    
    # Demo 2: Markdown conversion
    print("2. Markdown Conversion Demo")
    print("-" * 28)
    cmd = [sys.executable, "hwpx_to_markdown.py", 
           "examples/sample_document.hwpx", "examples/demo_markdown_output.md"]
    
    try:
        result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Markdown conversion completed successfully")
        else:
            print("✗ Markdown conversion failed")
            print(f"  Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Failed to run markdown conversion: {e}")
    
    print()
    
    # Demo 3: Table document (if available)
    if os.path.exists(table_file):
        print("3. Table Document Conversion Demo")
        print("-" * 34)
        cmd = [sys.executable, "hwpx_to_markdown.py", 
               "examples/table_document.hwpx", "examples/demo_table_output.md", 
               "--format-tables"]
        
        try:
            result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Table document conversion completed successfully")
                # Show the table output
                output_file = os.path.join(script_dir, "examples", "demo_table_output.md")
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print("  Generated markdown:")
                        for line in content.split('\n')[:10]:  # Show first 10 lines
                            print(f"    {line}")
            else:
                print("✗ Table document conversion failed")
                print(f"  Error: {result.stderr}")
        except Exception as e:
            print(f"✗ Failed to run table conversion: {e}")
        
        print()
    
    # Demo 4: Batch conversion
    print("4. Batch Conversion Demo")
    print("-" * 24)
    cmd = [sys.executable, "batch_conversion.py", 
           "examples/", "examples/demo_batch_output/", "--overwrite"]
    
    try:
        result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Batch conversion completed successfully")
            # List output files
            batch_dir = os.path.join(script_dir, "examples", "demo_batch_output")
            if os.path.exists(batch_dir):
                files = os.listdir(batch_dir)
                print(f"  Generated {len(files)} output files:")
                for file in sorted(files):
                    print(f"    - {file}")
        else:
            print("✗ Batch conversion failed")
            print(f"  Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Failed to run batch conversion: {e}")
    
    print()
    print("=" * 60)
    print("Demo completed! Check the examples/ directory for output files.")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    if not run_demo():
        sys.exit(1)