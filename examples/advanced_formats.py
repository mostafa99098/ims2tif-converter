#!/usr/bin/env python3
"""
Example: Advanced Export Formats
===============================

This example shows how to export in different formats using the advanced converter.
"""

from advanced_converter import AdvancedConverter

def advanced_formats_example():
    """Example of different export formats."""
    
    # Initialize the advanced converter
    converter = AdvancedConverter()
    
    ims_file = "path/to/your/file.ims"
    
    # Example 1: Standard 3D stack
    success1 = converter.convert_with_options(ims_file, "output/3d_stack.tif", "3d_stack")
    
    # Example 2: Individual Z-slices
    success2 = converter.convert_with_options(ims_file, "output/slices/", "individual_slices")
    
    # Example 3: OME-TIFF format
    success3 = converter.convert_with_options(ims_file, "output/ome_format.ome.tif", "ome_tiff")
    
    # Example 4: Compressed TIF
    success4 = converter.convert_with_options(ims_file, "output/compressed.tif", "compressed")
    
    print(f"3D Stack: {'Success' if success1 else 'Failed'}")
    print(f"Individual Slices: {'Success' if success2 else 'Failed'}")
    print(f"OME-TIFF: {'Success' if success3 else 'Failed'}")
    print(f"Compressed: {'Success' if success4 else 'Failed'}")

if __name__ == "__main__":
    advanced_formats_example()
