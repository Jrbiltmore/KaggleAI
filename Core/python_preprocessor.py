
"""
Python Preprocessor
-------------------
This script reads and preprocesses Python (.py) files from a specified directory,
applying specific tasks such as extracting comments or formatting code.

It demonstrates basic file reading and string manipulation techniques.
"""

import os
import re

def extract_comments_and_docstrings(file_content):
    """
    Extracts comments and docstrings from a Python file content.
    
    Args:
        file_content (str): Content of a Python file as a single string.
    
    Returns:
        str: Extracted comments and docstrings.
    """
    # Regex pattern for comments and docstrings (simplified)
    pattern = r'""".*?"""|\'\'\'.*?\'\'\'|#.*?$'
    matches = re.findall(pattern, file_content, re.DOTALL | re.MULTILINE)
    return "\n".join(matches)

def preprocess_python_file(file_path):
    """
    Reads a Python file, applies preprocessing tasks, and saves the processed content.
    
    Args:
        file_path (str): Path to the Python file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    processed_content = extract_comments_and_docstrings(content)
    
    # Save processed content to a new file (or update the original based on your needs)
    new_file_path = file_path.replace('.py', '_processed.py')
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(processed_content)
    print(f"Processed file saved to: {new_file_path}")

def process_directory(directory_path):
    """
    Searches for Python files in the specified directory and preprocesses each file.
    
    Args:
        directory_path (str): Path to the directory containing Python files.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith('.py'):
            file_path = os.path.join(directory_path, filename)
            preprocess_python_file(file_path)

# Example usage
if __name__ == "__main__":
    directory_path = 'path/to/your/python/files/directory'  # Update this to your directory path
    process_directory(directory_path)
