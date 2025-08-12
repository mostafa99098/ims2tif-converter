#!/usr/bin/env python3
"""
Example: Smart Filtering (Imaris-like)
=====================================

This example shows how to use smart filtering to match Imaris export behavior.
"""

from smart_converter import SmartConverter

def smart_filtering_example():
    """Example of smart filtering that matches Imaris behavior."""
    
    # Initialize the smart converter
    converter = SmartConverter()
    
    # Convert with smart filtering (removes empty Z-slices)
    ims_file = "path/to/your/file.ims"
    tif_file = "output/smart_filtered.tif"
    
    success = converter.convert_ims_to_tif_smart(
        ims_file, 
        tif_file, 
        filter_empty=True
    )
    
    if success:
        print(f"Smart conversion completed: {tif_file}")
        print("Empty Z-slices have been filtered out (like Imaris does)")
    else:
        print("Conversion failed")

if __name__ == "__main__":
    smart_filtering_example()
