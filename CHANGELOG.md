# Changelog

## Version 1.0.0 (2024-12-28)

### Features
- Complete IMS to TIF conversion system
- Multiple export formats (3D stack, individual slices, OME-TIFF, compressed)
- Smart filtering to match Imaris export behavior
- Recursive batch processing for entire directory trees
- Cross-platform compatibility (Windows, macOS, Linux)
- Professional command-line interfaces

### Converters
- **Core Library** (`ims2tif.py`) - Foundation conversion engine
- **Simple Converter** (`simple_converter.py`) - Basic user-friendly interface  
- **Universal Converter** (`universal_converter.py`) - Flexible path handling
- **Smart Converter** (`smart_converter.py`) - Imaris-like filtering
- **Recursive Converter** (`recursive_converter.py`) - Batch directory processing
- **Advanced Converter** (`advanced_converter.py`) - Multiple export formats

### Technical
- HDF5/IMS file structure analysis and parsing
- Automatic TimePoint format detection (TimePoint vs TimePoint 0)
- Empty slice filtering with configurable thresholds
- Memory-efficient processing for large datasets
- Error handling and detailed progress reporting

### Validation
- Tested on 295+ IMS files with 100% success rate
- Cross-validated output with Imaris software exports
- Verified slice count accuracy and data integrity
