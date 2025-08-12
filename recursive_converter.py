#!/usr/bin/env python3
"""
Recursive IMS to TIF Converter
==============================

Converts all IMS files in a directory tree (including subdirectories)
and saves TIF files in the same location as the original IMS files.
"""

import os
from pathlib import Path
from smart_converter import SmartConverter


class RecursiveConverter:
    """Converts all IMS files recursively through directory tree."""
    
    def __init__(self, use_smart_filtering=True):
        self.converter = SmartConverter()
        self.use_smart_filtering = use_smart_filtering
        self.stats = {
            'total_found': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'failed_files': []
        }
    
    def find_all_ims_files(self, root_directory):
        """Find all IMS files recursively in directory tree."""
        root_path = Path(root_directory)
        
        if not root_path.exists():
            raise ValueError(f"Directory not found: {root_directory}")
        
        # Find all .ims files recursively
        ims_files = list(root_path.rglob("*.ims"))
        
        print(f"🔍 Scanning directory tree: {root_directory}")
        print(f"Found {len(ims_files)} IMS files")
        
        # Group by directory for better organization
        by_directory = {}
        for ims_file in ims_files:
            dir_path = str(ims_file.parent)
            if dir_path not in by_directory:
                by_directory[dir_path] = []
            by_directory[dir_path].append(ims_file)
        
        print(f"Spread across {len(by_directory)} directories:")
        for directory, files in by_directory.items():
            rel_path = Path(directory).relative_to(root_path)
            print(f"   {rel_path}: {len(files)} files")
        
        return ims_files
    
    def convert_all_files(self, root_directory, overwrite=False):
        """Convert all IMS files in directory tree."""
        print("Recursive IMS to TIF Converter")
        print("=" * 40)
        
        # Find all IMS files
        ims_files = self.find_all_ims_files(root_directory)
        
        if not ims_files:
            print("No IMS files found!")
            return False
        
        self.stats['total_found'] = len(ims_files)
        
        print(f"\n🔄 Converting {len(ims_files)} files...")
        print(f"💡 Smart filtering: {'ON' if self.use_smart_filtering else 'OFF'}")
        print(f"🔄 Overwrite existing: {'YES' if overwrite else 'NO'}")
        print()
        
        # Convert each file
        for i, ims_file in enumerate(ims_files, 1):
            # Create TIF path in same directory as IMS file
            tif_file = ims_file.with_suffix('.tif')
            
            # Check if TIF already exists
            if tif_file.exists() and not overwrite:
                print(f"[{i}/{len(ims_files)}] ⏭️  SKIP: {ims_file.name} (TIF exists)")
                self.stats['skipped'] += 1
                continue
            
            print(f"[{i}/{len(ims_files)}] 🔄 {ims_file.name}")
            print(f"    {ims_file.parent}")
            
            try:
                if self.use_smart_filtering:
                    success = self.converter.convert_ims_to_tif_smart(
                        str(ims_file),
                        str(tif_file),
                        filter_empty=True
                    )
                else:
                    success = self.converter.convert_ims_to_tif(
                        str(ims_file),
                        str(tif_file)
                    )
                
                if success:
                    self.stats['successful'] += 1
                    print(f"    SUCCESS: {tif_file.name}")
                else:
                    self.stats['failed'] += 1
                    self.stats['failed_files'].append(str(ims_file))
                    print(f"    FAILED: {ims_file.name}")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.stats['failed_files'].append(str(ims_file))
                print(f"    ERROR: {str(e)[:80]}...")
            
            print()  # Empty line for readability
        
        # Print summary
        self.print_summary()
        return self.stats['successful'] > 0
    
    def print_summary(self):
        """Print conversion summary."""
        print("=" * 50)
        print("🎯 CONVERSION SUMMARY")
        print("=" * 50)
        print(f"📊 Total IMS files found: {self.stats['total_found']}")
        print(f"Successfully converted: {self.stats['successful']}")
        print(f"Failed conversions: {self.stats['failed']}")
        print(f"⏭️  Skipped (already exist): {self.stats['skipped']}")
        
        success_rate = (self.stats['successful'] / self.stats['total_found'] * 100) if self.stats['total_found'] > 0 else 0
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if self.stats['failed_files']:
            print("\nFailed files:")
            for failed_file in self.stats['failed_files']:
                print(f"   - {Path(failed_file).name}")


def main():
    """Interactive recursive converter."""
    print("🌳 Recursive IMS to TIF Converter")
    print("=" * 35)
    print("Converts all IMS files in directory tree (including subfolders)")
    print("Saves TIF files in the same location as original IMS files")
    print()
    
    # Get root directory
    default_dir = r"D:\Projects\dendrite\ImarisFiles4\imarisFilesSWC"
    print(f"Default directory: {default_dir}")
    root_dir = input("Enter root directory [press Enter for default]: ").strip().strip('"').strip("'")
    
    if not root_dir:
        root_dir = default_dir
    
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        return
    
    print(f"Using directory: {root_dir}")
    print()
    
    # Get options
    print("Options:")
    print("1. Smart filtering (removes empty Z-slices, like Imaris)")
    print("2. All slices (preserves complete data)")
    
    filtering_choice = input("Choose filtering option (1-2) [1]: ").strip()
    use_smart = filtering_choice != "2"
    
    overwrite_choice = input("Overwrite existing TIF files? (y/N): ").strip().lower()
    overwrite = overwrite_choice in ['y', 'yes']
    
    print(f"\n🔍 Preview mode - checking directory...")
    
    # Create converter and run
    converter = RecursiveConverter(use_smart_filtering=use_smart)
    
    try:
        # First, just show what would be converted
        ims_files = converter.find_all_ims_files(root_dir)
        
        if not ims_files:
            print("No IMS files found in directory tree!")
            return
        
        print(f"\nReady to convert {len(ims_files)} files")
        proceed = input("Proceed with conversion? (Y/n): ").strip().lower()
        
        if proceed in ['', 'y', 'yes']:
            print("\n" + "="*50)
            success = converter.convert_all_files(root_dir, overwrite=overwrite)
            
            if success:
                print("\nBatch conversion completed!")
            else:
                print("\nBatch conversion failed or no files processed!")
        else:
            print("⏹️  Conversion cancelled.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Conversion cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
