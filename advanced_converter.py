#!/usr/bin/env python3
"""
Advanced IMS to TIF Converter with Multiple Export Options
==========================================================

This script provides different export options to match various needs:
1. Full 3D stack (like our current script)
2. Individual Z-slice files (like some Imaris exports)
3. OME-TIFF format (like Imaris OME export)
4. Compressed formats
"""

import os
import sys
from pathlib import Path
import numpy as np
import tifffile
from ims2tif import IMS2TIFConverter


class AdvancedConverter(IMS2TIFConverter):
    """Advanced converter with multiple export options."""
    
    def convert_with_options(self, ims_path, output_path, export_type="3d_stack", **kwargs):
        """
        Convert IMS to TIF with different export options.
        
        Args:
            ims_path: Path to IMS file
            output_path: Output path (file or directory)
            export_type: Type of export
                - "3d_stack": Single TIF with all Z-slices (default)
                - "individual_slices": Separate TIF for each Z-slice
                - "ome_tiff": OME-TIFF format
                - "compressed": Compressed 3D stack
            **kwargs: Additional parameters (channel, timepoint, etc.)
        """
        
        # First, get the image data using parent class
        import h5py
        
        try:
            with h5py.File(ims_path, 'r') as f:
                print(f"Reading IMS file: {ims_path}")
                
                # Navigate to data (using fixed logic from parent class)
                dataset = f['DataSet']
                resolution_levels = [k for k in dataset.keys() if k.startswith('ResolutionLevel')]
                if not resolution_levels:
                    raise ValueError("No resolution levels found")
                
                res_level_path = f'DataSet/ResolutionLevel 0'
                res_level = f[res_level_path]
                timepoint_keys = [k for k in res_level.keys() if k.startswith('TimePoint')]
                
                if not timepoint_keys:
                    raise ValueError("No TimePoint data found")
                
                # Select timepoint
                tp_key = timepoint_keys[kwargs.get('timepoint', 0)] if kwargs.get('timepoint') is not None else timepoint_keys[0]
                tp_path = f"{res_level_path}/{tp_key}"
                
                # Select channel
                tp_group = f[tp_path]
                channel_keys = [k for k in tp_group.keys() if k.startswith('Channel')]
                if not channel_keys:
                    raise ValueError("No Channel data found")
                
                ch_key = channel_keys[kwargs.get('channel', 0)] if kwargs.get('channel') is not None else channel_keys[0]
                data_path = f"{tp_path}/{ch_key}/Data"
                
                # Read image data
                image_data = f[data_path][:]
                print(f"Image shape: {image_data.shape}")
                print(f"Data type: {image_data.dtype}")
                
                # Export based on type
                if export_type == "3d_stack":
                    return self._export_3d_stack(image_data, output_path)
                    
                elif export_type == "individual_slices":
                    return self._export_individual_slices(image_data, output_path, ims_path)
                    
                elif export_type == "ome_tiff":
                    return self._export_ome_tiff(image_data, output_path)
                    
                elif export_type == "compressed":
                    return self._export_compressed(image_data, output_path)
                    
                else:
                    raise ValueError(f"Unknown export type: {export_type}")
                    
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def _export_3d_stack(self, image_data, output_path):
        """Export as single 3D TIF stack (our current method)."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tifffile.imwrite(output_path, image_data)
        print(f"3D stack saved: {output_path}")
        print(f"   Shape: {image_data.shape} ({image_data.shape[0]} Z-slices)")
        return True
    
    def _export_individual_slices(self, image_data, output_base, ims_path):
        """Export each Z-slice as individual TIF file (like some Imaris exports)."""
        base_name = Path(ims_path).stem
        output_dir = Path(output_base).parent / f"{base_name}_slices"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        num_slices = image_data.shape[0]
        print(f"Exporting {num_slices} individual Z-slices...")
        
        for z in range(num_slices):
            slice_data = image_data[z]
            slice_file = output_dir / f"{base_name}_z{z:03d}.tif"
            tifffile.imwrite(slice_file, slice_data)
            
        print(f"   Saved {num_slices} files in: {output_dir}")
        print(f"   Each slice shape: {slice_data.shape}")
        return True
    
    def _export_ome_tiff(self, image_data, output_path):
        """Export as OME-TIFF format (like Imaris OME export)."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create OME metadata
        metadata = {
            'axes': 'ZYX',
            'Channel': {'Name': 'Channel 0'},
            'PhysicalSizeX': 1.0,
            'PhysicalSizeY': 1.0, 
            'PhysicalSizeZ': 1.0,
            'PhysicalSizeXUnit': 'µm',
            'PhysicalSizeYUnit': 'µm',
            'PhysicalSizeZUnit': 'µm'
        }
        
        tifffile.imwrite(
            output_path, 
            image_data,
            metadata=metadata,
            compression='lzw'  # Add compression
        )
        print(f"OME-TIFF saved: {output_path}")
        print(f"   Shape: {image_data.shape} with OME metadata")
        return True
    
    def _export_compressed(self, image_data, output_path):
        """Export as compressed TIF (smaller file size)."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        tifffile.imwrite(
            output_path, 
            image_data,
            compression='lzw',  # LZW compression
            predictor=True      # Better compression for scientific data
        )
        print(f"Compressed TIF saved: {output_path}")
        print(f"   Shape: {image_data.shape} (LZW compressed)")
        return True


def main():
    """Interactive converter with export options."""
    print("🔬 Advanced IMS to TIF Converter")
    print("=" * 40)
    print()
    print("Export Options:")
    print("1. 3D Stack (single TIF with all Z-slices)")
    print("2. Individual Slices (separate TIF for each Z-slice)")  
    print("3. OME-TIFF (Open Microscopy format)")
    print("4. Compressed (smaller file size)")
    print()
    
    # Get input file
    ims_file = input("Enter IMS file path: ").strip().strip('"').strip("'")
    if not os.path.exists(ims_file):
        print(f"File not found: {ims_file}")
        return
    
    # Get export type
    choice = input("Choose export type (1-4) [1]: ").strip()
    if not choice:
        choice = "1"
    
    export_types = {
        "1": "3d_stack",
        "2": "individual_slices", 
        "3": "ome_tiff",
        "4": "compressed"
    }
    
    if choice not in export_types:
        print("Invalid choice")
        return
    
    export_type = export_types[choice]
    
    # Generate output path
    ims_path = Path(ims_file)
    if export_type == "individual_slices":
        output_path = f"advanced_output/{ims_path.stem}_slices"
    else:
        output_path = f"advanced_output/{ims_path.stem}_{export_type}.tif"
    
    # Convert
    converter = AdvancedConverter()
    print(f"\nConverting with {export_type} format...")
    
    success = converter.convert_with_options(
        ims_file,
        output_path,
        export_type=export_type
    )
    
    if success:
        print("\nConversion completed!")
        print(f"Output: {os.path.abspath(output_path)}")
    else:
        print("\nConversion failed!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
