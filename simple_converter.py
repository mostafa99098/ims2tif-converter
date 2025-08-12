#!/usr/bin/env python3
"""
Simple IMS Converter
===================

Basic converter for converting all IMS files in a directory to TIF format.
User-friendly interface with minimal configuration required.
"""

import os
from pathlib import Path
from ims2tif import IMS2TIFConverter


def simple_convert():
    """Simple directory converter with minimal prompts."""
    
    print("IMS to TIF Converter")
    print("=" * 25)
    
    # Get directory from user
    print("Enter the full path to your IMS files directory:")
    print("(You can copy-paste the path)")
    print()
    
    directory = input("Directory: ").strip().strip('"').strip("'")
    
    if not directory:
        print("Error: No directory specified.")
        return
    
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return
    
    # Find IMS files
    ims_files = list(Path(directory).glob("*.ims"))
    
    if not ims_files:
        print(f"Error: No IMS files found in: {directory}")
        return
    
    print(f"Found {len(ims_files)} IMS files")
    
    # Create output folder
    output_dir = "converted_tif_files"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert files
    converter = IMS2TIFConverter()
    print("\nStarting conversion...")
    
    for i, ims_file in enumerate(ims_files, 1):
        print(f"[{i}/{len(ims_files)}] {ims_file.name}... ", end="")
        
        output_file = Path(output_dir) / f"{ims_file.stem}.tif"
        
        try:
            success = converter.convert_ims_to_tif(str(ims_file), str(output_file))
            print("SUCCESS" if success else "FAILED")
        except Exception:
            print("FAILED")
    
    print(f"\nComplete! Check the '{output_dir}' folder for your TIF files.")
    print(f"Full path: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    try:
        simple_convert()
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
