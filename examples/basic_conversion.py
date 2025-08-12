#!/usr/bin/env python3
"""
Example: Basic IMS to TIF Conversion
===================================

This example shows the simplest way to convert IMS files to TIF format.
"""

from ims2tif import IMS2TIFConverter

def basic_conversion_example():
    """Example of basic IMS to TIF conversion."""
    
    # Initialize the converter
    converter = IMS2TIFConverter()
    
    # Convert a single file
    ims_file = "path/to/your/file.ims"
    tif_file = "output/converted_file.tif"
    
    success = converter.convert_ims_to_tif(ims_file, tif_file)
    
    if success:
        print(f"Successfully converted {ims_file} to {tif_file}")
    else:
        print("Conversion failed")

if __name__ == "__main__":
    basic_conversion_example()
