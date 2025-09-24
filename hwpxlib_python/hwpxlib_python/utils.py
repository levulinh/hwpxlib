"""
Utility functions for HWPX processing.

This module contains utility functions for setting up the Java environment
and handling JPype integration.
"""

import os
import subprocess
import jpype
import jpype.imports
from jpype.types import *


def setup_java_environment(jar_path=None):
    """
    Initialize JPype and setup the Java classpath with robust JVM detection.
    
    Args:
        jar_path (str, optional): Path to the hwpxlib JAR file. If None, will auto-detect.
        
    Returns:
        str: Path to the JAR file being used
        
    Raises:
        FileNotFoundError: If the JAR file cannot be found
        RuntimeError: If JVM initialization fails
    """
    if jar_path is None:
        # Auto-detect JAR path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Look for JAR in several locations
        possible_paths = [
            # If installed as part of the main project
            os.path.join(current_dir, '..', '..', 'target', 'hwpxlib-1.0.7.jar'),
            # If in development
            os.path.join(current_dir, '..', '..', '..', 'target', 'hwpxlib-1.0.7.jar'),
            # Environment variable
            os.environ.get('HWPXLIB_JAR_PATH', '')
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                jar_path = os.path.abspath(path)
                break
        
        if not jar_path or not os.path.exists(jar_path):
            raise FileNotFoundError(
                "JAR file not found. Please either:\n"
                "1. Build the project with: mvn clean package\n"
                "2. Set HWPXLIB_JAR_PATH environment variable\n"
                "3. Pass jar_path parameter to this function"
            )
    
    if not jpype.isJVMStarted():
        # Try to find the correct JVM path, especially important on macOS
        jvm_path = None
        
        # First, try to get JAVA_HOME from environment
        java_home = os.environ.get('JAVA_HOME')
        if java_home and os.path.exists(java_home):
            # Look for the JVM library in common locations
            possible_jvm_paths = [
                os.path.join(java_home, 'lib', 'server', 'libjvm.dylib'),  # macOS
                os.path.join(java_home, 'lib', 'server', 'libjvm.so'),     # Linux
                os.path.join(java_home, 'bin', 'server', 'jvm.dll'),       # Windows
                os.path.join(java_home, 'jre', 'lib', 'server', 'libjvm.dylib'),  # macOS older versions
                os.path.join(java_home, 'jre', 'lib', 'server', 'libjvm.so'),     # Linux older versions
            ]
            
            for path in possible_jvm_paths:
                if os.path.exists(path):
                    jvm_path = path
                    break
        
        # If JAVA_HOME didn't work, try to detect using java command
        if not jvm_path:
            try:
                # Use java -XshowSettings:properties to get java.home
                result = subprocess.run(['java', '-XshowSettings:properties', '-version'], 
                                      capture_output=True, text=True)
                # Java prints properties to stderr, so check both stdout and stderr
                output = result.stderr + result.stdout
                if result.returncode == 0:
                    for line in output.split('\n'):
                        if 'java.home' in line:
                            java_home = line.split('=')[-1].strip()
                            # Look for JVM library
                            possible_jvm_paths = [
                                os.path.join(java_home, 'lib', 'server', 'libjvm.dylib'),  # macOS
                                os.path.join(java_home, 'lib', 'server', 'libjvm.so'),     # Linux
                                os.path.join(java_home, 'bin', 'server', 'jvm.dll'),       # Windows
                            ]
                            
                            for path in possible_jvm_paths:
                                if os.path.exists(path):
                                    jvm_path = path
                                    break
                            break
            except:
                pass  # Fall back to default JPype detection
        
        # Start JVM with explicit path if found, otherwise let JPype auto-detect
        try:
            if jvm_path:
                jpype.startJVM(jvm_path, classpath=[jar_path])
            else:
                jpype.startJVM(classpath=[jar_path])
        except Exception as e:
            # If JPype fails, provide helpful error message
            raise RuntimeError(f"Failed to start JVM: {e}\n"
                             f"This often happens on macOS when the wrong JVM is detected.\n"
                             f"Try setting JAVA_HOME environment variable to your JDK installation.\n"
                             f"For example: export JAVA_HOME=$(/usr/libexec/java_home)")
    
    return jar_path


def shutdown_java_environment():
    """
    Shutdown the JPype JVM.
    
    Note: This is usually not necessary as the JVM will shutdown automatically
    when Python exits, but can be useful for cleanup in some scenarios.
    """
    if jpype.isJVMStarted():
        jpype.shutdownJVM()