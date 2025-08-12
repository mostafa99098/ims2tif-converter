#!/usr/bin/env python3
"""
IMS to TIF Converter
===================

Core library for converting Imaris IMS files to TIF format.
Supports multi-channel, multi-timepoint, and multi-Z-slice data.

Dependencies:
- h5py: For reading IMS files (HDF5 format)
- tifffile: For writing TIF files
- numpy: For array operations
- argparse: For command line interface

Usage:
    python ims2tif.py input.ims output.tif [options]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import h5py
    import numpy as np
    import tifffile
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required packages:")
    print("pip install h5py tifffile numpy")
    sys.exit(1)


class IMS2TIFConverter:
    """Converter class for IMS to TIF format conversion."""
    
    def __init__(self):
        self.supported_extensions = ['.ims']
    
    def is_ims_file(self, file_path):
        """Check if the file is a valid IMS file."""
        return Path(file_path).suffix.lower() in self.supported_extensions
    
    def read_ims_metadata(self, ims_file):
        """Read metadata from IMS file."""
        metadata = {}
        try:
            with h5py.File(ims_file, 'r') as f:
                # Common IMS metadata locations
                if 'DataSetInfo' in f:
                    dataset_info = f['DataSetInfo']
                    if 'Image' in dataset_info.attrs:
                        metadata['image_info'] = dataset_info.attrs['Image']
                
                # Get dataset information
                if 'DataSet' in f:
                    dataset = f['DataSet']
                    metadata['dataset_keys'] = list(dataset.keys())
                    
                    # Get resolution levels
                    resolution_levels = [k for k in dataset.keys() if k.startswith('ResolutionLevel')]
                    metadata['resolution_levels'] = resolution_levels
                    
                    if resolution_levels:
                        # Get data from highest resolution
                        highest_res = f'DataSet/{resolution_levels[0]}'
                        if 'TimePoint' in f[highest_res]:
                            timepoints = list(f[highest_res]['TimePoint'].keys())
                            metadata['timepoints'] = timepoints
                            
                            if timepoints:
                                # Get channel information
                                first_timepoint = f'{highest_res}/TimePoint/{timepoints[0]}'
                                if 'Channel' in f[first_timepoint]:
                                    channels = list(f[first_timepoint]['Channel'].keys())
                                    metadata['channels'] = channels
                
        except Exception as e:
            print(f"Warning: Could not read all metadata: {e}")
        
        return metadata
    
    def convert_ims_to_tif(self, ims_path, tif_path, channel=None, timepoint=None, z_slice=None):
        """
        Convert IMS file to TIF format.
        
        Args:
            ims_path (str): Path to input IMS file
            tif_path (str): Path to output TIF file
            channel (int, optional): Specific channel to extract (0-based)
            timepoint (int, optional): Specific timepoint to extract (0-based)
            z_slice (int, optional): Specific Z slice to extract (0-based)
        """
        try:
            with h5py.File(ims_path, 'r') as f:
                print(f"Reading IMS file: {ims_path}")
                
                # Read metadata
                metadata = self.read_ims_metadata(ims_path)
                print(f"Found metadata: {metadata}")
                
                # Navigate to data
                dataset = f['DataSet']
                
                # Get highest resolution data
                resolution_levels = [k for k in dataset.keys() if k.startswith('ResolutionLevel')]
                if not resolution_levels:
                    raise ValueError("No resolution levels found in IMS file")
                
                # Use highest resolution (ResolutionLevel 0)
                res_level_path = f'DataSet/ResolutionLevel 0'
                
                if res_level_path.replace('DataSet/', '') not in dataset:
                    raise ValueError("ResolutionLevel 0 not found")
                
                # Check for TimePoint data - handle both 'TimePoint' and 'TimePoint 0' formats
                res_level = f[res_level_path]
                timepoint_keys = [k for k in res_level.keys() if k.startswith('TimePoint')]
                
                if not timepoint_keys:
                    raise ValueError("No TimePoint data found")
                
                if not timepoint_keys:
                    raise ValueError("No TimePoint data found")
                
                # Select timepoint
                if timepoint is not None:
                    # Look for specific timepoint
                    target_tp = f'TimePoint {timepoint}'
                    if target_tp in timepoint_keys:
                        tp_key = target_tp
                    elif timepoint < len(timepoint_keys):
                        tp_key = timepoint_keys[timepoint]
                    else:
                        raise ValueError(f"Timepoint {timepoint} not available. Available: {timepoint_keys}")
                else:
                    tp_key = timepoint_keys[0]  # Use first timepoint
                
                tp_path = f"{res_level_path}/{tp_key}"
                
                if tp_key not in res_level:
                    raise ValueError(f"TimePoint {tp_key} not found")
                
                # Check for Channel data
                tp_group = f[tp_path]
                channel_keys = [k for k in tp_group.keys() if k.startswith('Channel')]
                
                if not channel_keys:
                    raise ValueError("No Channel data found")
                
                if not channel_keys:
                    raise ValueError("No channels found")
                
                # Select channel
                if channel is not None:
                    # Look for specific channel
                    target_ch = f'Channel {channel}'
                    if target_ch in channel_keys:
                        ch_key = target_ch
                    elif channel < len(channel_keys):
                        ch_key = channel_keys[channel]
                    else:
                        raise ValueError(f"Channel {channel} not available. Available: {channel_keys}")
                else:
                    ch_key = channel_keys[0]  # Use first channel
                
                data_path = f"{tp_path}/{ch_key}/Data"
                
                if 'Data' not in f[f"{tp_path}/{ch_key}"]:
                    raise ValueError("No image data found")
                
                # Read the image data
                image_data = f[data_path][:]
                
                print(f"Image shape: {image_data.shape}")
                print(f"Data type: {image_data.dtype}")
                
                # Handle Z slice selection
                if z_slice is not None and len(image_data.shape) >= 3:
                    if z_slice >= image_data.shape[0]:
                        raise ValueError(f"Z slice {z_slice} not available. Max: {image_data.shape[0]-1}")
                    image_data = image_data[z_slice]
                
                # Ensure output directory exists
                os.makedirs(os.path.dirname(tif_path), exist_ok=True)
                
                # Write TIF file
                print(f"Writing TIF file: {tif_path}")
                tifffile.imwrite(tif_path, image_data)
                
                print(f"Successfully converted {ims_path} to {tif_path}")
                return True
                
        except Exception as e:
            print(f"Error converting file: {e}")
            return False


def main():
    """Main function for command line interface."""
    parser = argparse.ArgumentParser(
        description="Convert Imaris IMS files to TIF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python ims2tif.py input.ims output.tif
    python ims2tif.py input.ims output.tif --channel 0 --timepoint 0
    python ims2tif.py input.ims output.tif --z-slice 10
        """
    )
    
    parser.add_argument('input', help='Input IMS file path')
    parser.add_argument('output', help='Output TIF file path')
    parser.add_argument('--channel', type=int, help='Channel to extract (0-based index)')
    parser.add_argument('--timepoint', type=int, help='Timepoint to extract (0-based index)')
    parser.add_argument('--z-slice', type=int, help='Z slice to extract (0-based index)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}")
        sys.exit(1)
    
    # Create converter instance
    converter = IMS2TIFConverter()
    
    # Check if input is IMS file
    if not converter.is_ims_file(args.input):
        print(f"Warning: Input file may not be a valid IMS file: {args.input}")
    
    # Perform conversion
    success = converter.convert_ims_to_tif(
        args.input,
        args.output,
        channel=args.channel,
        timepoint=args.timepoint,
        z_slice=args.z_slice
    )
    
    if success:
        print("Conversion completed successfully!")
        sys.exit(0)
    else:
        print("Conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
