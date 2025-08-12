# IMS to TIF Converter

A Python toolkit for converting Imaris IMS files to TIF format. Supports multiple conversion modes, batch processing, and integration with scientific imaging workflows.

## Features

- Convert single or multiple IMS files to TIF format
- Smart filtering to remove empty Z-slices (matches Imaris behavior)
- Batch processing with recursive directory scanning
- Multiple output formats (standard TIF, OME-TIFF, compressed)
- Individual Z-slice export option
- Preserves image metadata and data integrity
- Command-line and programmatic interfaces

## Requirements

- Python 3.7 or higher
- Required packages (install with `pip install -r requirements.txt`):
  - h5py (for reading IMS files)
  - tifffile (for writing TIF files)
  - numpy (for array operations)
  - imagecodecs (for compression support)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ims2tif-converter.git
   cd ims2tif-converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Simple Conversion
```bash
python simple_converter.py
```
Enter your directory path when prompted. Converts all IMS files to TIF format.

### Universal Converter
```bash
# Interactive mode
python universal_converter.py

# Command line mode
python universal_converter.py "path/to/ims/files" "path/to/output"
```

### Smart Converter (Removes Empty Slices)
```bash
python smart_converter.py
```
Automatically filters out empty Z-slices, similar to Imaris export behavior.

### Batch Processing
```bash
python recursive_converter.py
```
Recursively processes all IMS files in a directory tree, saving TIF files alongside originals.

### Advanced Options
```bash
python advanced_converter.py
```
Multiple export formats including:
- 3D TIF stacks
- Individual Z-slice files
- OME-TIFF format
- Compressed TIF files

## File Structure

```
ims2tif/
├── simple_converter.py       # Basic directory conversion
├── universal_converter.py    # Full-featured converter
├── smart_converter.py        # Imaris-like filtering
├── recursive_converter.py    # Batch processing
├── advanced_converter.py     # Multiple export formats
├── ims2tif.py               # Core conversion library
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Core Library

The `ims2tif.py` module provides the base conversion functionality and can be used programmatically:

```python
from ims2tif import IMS2TIFConverter

converter = IMS2TIFConverter()
success = converter.convert_ims_to_tif(
    'input.ims',
    'output.tif',
    channel=0,
    timepoint=0
)
```

## IMS File Format

IMS files are Imaris native format files that use HDF5 structure. This converter:

- Reads the HDF5 structure of IMS files
- Extracts image data from the highest resolution level
- Supports multi-dimensional data (X, Y, Z, C, T)
- Preserves data types and ranges

## Output Compatibility

The converted TIF files can be opened in:
- ImageJ/Fiji
- Adobe Photoshop
- GIMP
- MATLAB
- Python (PIL, opencv, scikit-image)
- Any software supporting TIF format

## Performance

- Tested with 295+ IMS files
- Handles files with varying Z-slice counts (24-64 slices)
- Smart filtering reduces file sizes by removing empty slices
- Batch processing capability for large datasets

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Install required packages with `pip install -r requirements.txt`

2. **File access errors**: Ensure you have read permissions for input files and write permissions for output directories

3. **Memory issues with large files**: For very large IMS files, consider processing individual channels or timepoints

4. **Unsupported IMS structure**: Some IMS files may have non-standard structures. Check the metadata first:
   ```python
   converter = IMS2TIFConverter()
   metadata = converter.read_ims_metadata('your_file.ims')
   print(metadata)
   ```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source. Please check with your institution regarding any licensing requirements for scientific software.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the example usage in each converter script
3. Submit an issue with details about your IMS file structure and error messages
