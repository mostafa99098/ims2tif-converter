#!/usr/bin/env python3
"""
Example: Batch Processing Directory
==================================

This example shows how to process all IMS files in a directory tree.
"""

from recursive_converter import RecursiveConverter

def batch_processing_example():
    """Example of batch processing multiple IMS files."""
    
    # Set up path
    input_directory = "path/to/ims/files"  # Change this to your directory
    
    # Initialize the recursive converter
    converter = RecursiveConverter()
    
    # Convert all files in directory (automatically finds IMS files)
    success = converter.convert_all_files(input_directory, overwrite=False)
    
    # Print results
    converter.print_summary()
    
    if success:
        print("Batch conversion completed successfully!")
    else:
        print("Some conversions failed. Check the summary above.")

if __name__ == "__main__":
    batch_processing_example()
