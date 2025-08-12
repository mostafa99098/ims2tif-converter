#!/usr/bin/env python3
"""
Smart IMS to TIF Converter - Matches Imaris Behavior
====================================================

This converter automatically filters out empty Z-slices,
just like Imaris does when exporting TIF files.
"""

import os
import numpy as np
import tifffile
from ims2tif import IMS2TIFConverter


class SmartConverter(IMS2TIFConverter):
    """Converter that filters empty slices like Imaris."""
    
    def convert_ims_to_tif_smart(self, ims_path, tif_path, 
                                empty_threshold=10, 
                                filter_empty=True,
                                **kwargs):
        """
        Convert IMS to TIF with smart empty slice filtering.
        
        Args:
            ims_path: Input IMS file
            tif_path: Output TIF file
            empty_threshold: Pixel value threshold for empty slices
            filter_empty: Whether to filter out empty slices
            **kwargs: Other parameters (channel, timepoint, etc.)
        """
        
        try:
            import h5py
            
            with h5py.File(ims_path, 'r') as f:
                print(f"Reading IMS file: {ims_path}")
                
                # Get data using existing logic
                dataset = f['DataSet']
                res_level_path = f'DataSet/ResolutionLevel 0'
                res_level = f[res_level_path]
                timepoint_keys = [k for k in res_level.keys() if k.startswith('TimePoint')]
                
                if not timepoint_keys:
                    raise ValueError("No TimePoint data found")
                
                tp_key = timepoint_keys[kwargs.get('timepoint', 0)] if kwargs.get('timepoint') is not None else timepoint_keys[0]
                tp_path = f"{res_level_path}/{tp_key}"
                
                tp_group = f[tp_path]
                channel_keys = [k for k in tp_group.keys() if k.startswith('Channel')]
                if not channel_keys:
                    raise ValueError("No Channel data found")
                
                ch_key = channel_keys[kwargs.get('channel', 0)] if kwargs.get('channel') is not None else channel_keys[0]
                data_path = f"{tp_path}/{ch_key}/Data"
                
                # Read image data
                image_data = f[data_path][:]
                print(f"Original shape: {image_data.shape}")
                print(f"Data type: {image_data.dtype}")
                
                if filter_empty:
                    # Analyze Z-slices for empty content
                    non_empty_indices = []
                    empty_indices = []
                    
                    for z in range(image_data.shape[0]):
                        slice_max = image_data[z].max()
                        if slice_max > empty_threshold:
                            non_empty_indices.append(z)
                        else:
                            empty_indices.append(z)
                    
                    print(f"Analysis:")
                    print(f"  Total Z-slices: {image_data.shape[0]}")
                    print(f"  Non-empty slices: {len(non_empty_indices)} (max > {empty_threshold})")
                    print(f"  Empty slices: {len(empty_indices)}")
                    
                    if non_empty_indices:
                        # Extract only non-empty slices
                        filtered_data = image_data[non_empty_indices]
                        print(f"Filtered shape: {filtered_data.shape}")
                        print(f"Removed {len(empty_indices)} empty slices")
                        
                        # Use filtered data
                        final_data = filtered_data
                    else:
                        print("Warning: No non-empty slices found, using all data")
                        final_data = image_data
                else:
                    final_data = image_data
                
                # Save TIF file
                os.makedirs(os.path.dirname(tif_path), exist_ok=True)
                print(f"Writing TIF file: {tif_path}")
                tifffile.imwrite(tif_path, final_data)
                
                print("Successfully converted!")
                print(f"   Input: {image_data.shape[0]} slices")
                print(f"   Output: {final_data.shape[0]} slices")
                print(f"   File: {tif_path}")
                
                return True
                
        except Exception as e:
            print(f"Error: {e}")
            return False


def main():
    """Interactive smart converter."""
    print("Smart IMS to TIF Converter (Imaris-like)")
    print("=" * 45)
    print("This converter filters empty Z-slices like Imaris does.")
    print()
    
    # Get input
    ims_file = input("Enter IMS file path: ").strip().strip('"').strip("'")
    if not os.path.exists(ims_file):
        print(f"File not found: {ims_file}")
        return
    
    # Get output path
    from pathlib import Path
    default_output = f"smart_output/{Path(ims_file).stem}_smart.tif"
    output_file = input(f"Output path [{default_output}]: ").strip().strip('"').strip("'")
    if not output_file:
        output_file = default_output
    
    # Options
    print("\nOptions:")
    print("1. Smart filtering (like Imaris) - removes empty slices")
    print("2. All slices (like our original script)")
    
    choice = input("Choose option (1-2) [1]: ").strip()
    filter_empty = choice != "2"
    
    # Convert
    converter = SmartConverter()
    print(f"\n🚀 Converting with {'smart filtering' if filter_empty else 'all slices'}...")
    
    success = converter.convert_ims_to_tif_smart(
        ims_file,
        output_file,
        filter_empty=filter_empty
    )
    
    if success:
        print("\nConversion completed!")
        print(f"Output: {os.path.abspath(output_file)}")
    else:
        print("\nConversion failed!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
