#!/usr/bin/env python3
"""
Setup Script for HWPX to Markdown Conversion Tools

This script helps set up the environment for running the Python sample scripts.

Usage:
    python setup.py [--install-deps]

Author: Generated for hwpxlib project
License: Apache-2.0
"""

import sys
import os
import subprocess
import argparse


def check_java():
    """Check if Java is installed."""
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            # Java version is in stderr for some reason
            version_info = result.stderr.split('\n')[0] if result.stderr else result.stdout.split('\n')[0]
            print(f"✓ Java is installed: {version_info.strip()}")
            return True
        else:
            print("✗ Java is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("✗ Java is not installed or not in PATH")
        return False


def check_mvn():
    """Check if Maven is installed."""
    try:
        result = subprocess.run(['mvn', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_info = result.stdout.split('\n')[0]
            print(f"✓ Maven is installed: {version_info}")
            return True
        else:
            print("✗ Maven is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("✗ Maven is not installed or not in PATH")
        return False


def build_jar():
    """Build the Java JAR file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print("\nBuilding Java JAR file...")
    try:
        result = subprocess.run(['mvn', 'clean', 'package', '-DskipTests'], 
                              cwd=project_root, 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            jar_path = os.path.join(project_root, "target", "hwpxlib-1.0.7.jar")
            if os.path.exists(jar_path):
                print(f"✓ JAR file built successfully: {jar_path}")
                return True
            else:
                print("✗ JAR file was not created")
                return False
        else:
            print("✗ Failed to build JAR file")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Failed to build JAR file: {e}")
        return False


def install_python_deps():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Python dependencies installed successfully")
            return True
        else:
            print("✗ Failed to install Python dependencies")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Failed to install Python dependencies: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Setup HWPX to Markdown conversion tools')
    parser.add_argument('--install-deps', action='store_true', 
                       help='Automatically install Python dependencies')
    
    args = parser.parse_args()
    
    print("HWPX to Markdown Conversion Tools - Setup")
    print("=" * 50)
    
    # Check system prerequisites
    print("Checking system prerequisites...")
    java_ok = check_java()
    mvn_ok = check_mvn()
    
    if not java_ok:
        print("\nPlease install Java Development Kit (JDK) 7 or later")
        print("Download from: https://adoptium.net/")
        return False
    
    if not mvn_ok:
        print("\nPlease install Apache Maven")
        print("Download from: https://maven.apache.org/download.cgi")
        return False
    
    # Build JAR file
    if not build_jar():
        return False
    
    # Install Python dependencies if requested
    if args.install_deps:
        if not install_python_deps():
            return False
    else:
        print("\nTo install Python dependencies, run:")
        print("  python setup.py --install-deps")
        print("or manually:")
        print("  pip install -r requirements.txt")
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("You can now run the demo with: python demo.py")
    
    return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)