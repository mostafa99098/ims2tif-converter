#!/usr/bin/env python3
"""
Universal IMS to TIF Converter
=============================

Flexible script to convert IMS files from any directory to TIF format.

Usage:
    python universal_converter.py
    python universal_converter.py "path/to/ims/files"
    python universal_converter.py "path/to/ims/files" "path/to/output"
"""

import os
import sys
from pathlib import Path
from ims2tif import IMS2TIFConverter


def get_input_directory():
    """Get input directory from user or command line."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    print("Universal IMS to TIF Converter")
    print("=" * 35)
    print()
    print("Please enter the path to your IMS files directory:")
    print("Examples:")
    print(r'  D:\Projects\dendrite\ImarisFiles4\imarisFilesSWC\v03_i02')
    print(r'  C:\MyData\IMS_Files')
    print("  /home/user/ims_data")
    print()
    
    while True:
        user_input = input("Directory path: ").strip().strip('"').strip("'")
        
        if user_input:
            if Path(user_input).exists():
                return user_input
            else:
                print(f"Directory not found: {user_input}")
                print("Please try again or check the path.")
                continue
        else:
            print("Please enter a valid directory path.")


def get_output_directory(input_dir):
    """Get output directory from user or command line."""
    if len(sys.argv) > 2:
        return sys.argv[2]
    
    # Default output directory based on input
    input_name = Path(input_dir).name
    default_output = f"converted_tif_{input_name}"
    
    print(f"\nOutput directory (press Enter for default: {default_output}):")
    user_output = input("Output path: ").strip().strip('"').strip("'")
    
    return user_output if user_output else default_output


def convert_directory(input_directory, output_directory):
    """Convert all IMS files in a directory to TIF format."""
    
    print(f"\nProcessing Directory: {input_directory}")
    print(f"Output Directory: {output_directory}")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_directory, exist_ok=True)
    
    # Find all IMS files
    input_path = Path(input_directory)
    ims_files = list(input_path.glob("*.ims"))
    
    if not ims_files:
        print("No IMS files found in the specified directory.")
        return False
    
    print(f"Found {len(ims_files)} IMS file(s):")
    for i, ims_file in enumerate(ims_files, 1):
        print(f"  {i}. {ims_file.name}")
    print()
    
    # Initialize converter
    converter = IMS2TIFConverter()
    
    successful = 0
    failed = 0
    failed_files = []
    
    for i, ims_file in enumerate(ims_files, 1):
        print(f"[{i}/{len(ims_files)}] Converting: {ims_file.name}")
        
        # Create output filename
        output_file = Path(output_directory) / f"{ims_file.stem}.tif"
        
        try:
            success = converter.convert_ims_to_tif(
                str(ims_file),
                str(output_file)
            )
            
            if success:
                successful += 1
                print(f"  ✓ Success: {output_file.name}")
            else:
                failed += 1
                failed_files.append(ims_file.name)
                print(f"  ✗ Failed: {ims_file.name}")
                
        except Exception as e:
            failed += 1
            failed_files.append(ims_file.name)
            print(f"  ✗ Error: {str(e)[:100]}...")
    
    # Summary
    print("\n" + "=" * 50)
    print("CONVERSION SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {len(ims_files)}")
    print(f"Successful conversions: {successful}")
    print(f"Failed conversions: {failed}")
    print(f"Output location: {os.path.abspath(output_directory)}")
    
    if failed_files:
        print(f"\nFailed files:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")
    
    return successful > 0


def main():
    """Main function."""
    try:
        # Get input directory
        input_dir = get_input_directory()
        if not input_dir:
            print("No input directory specified. Exiting.")
            return
        
        # Get output directory
        output_dir = get_output_directory(input_dir)
        
        # Perform conversion
        success = convert_directory(input_dir, output_dir)
        
        if success:
            print("\nConversion completed!")
            print(f"Check your TIF files in: {os.path.abspath(output_dir)}")
        else:
            print("\nConversion failed or no files processed.")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
