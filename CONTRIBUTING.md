# Contributing to IMS2TIF Converter

We welcome contributions to improve the IMS2TIF Converter project!

## How to Contribute

### Reporting Issues
- Check existing issues before creating new ones
- Provide detailed information about your system and the problem
- Include sample IMS files if possible (for reproducible bugs)

### Development Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`

### Code Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for new functions and classes
- Include error handling for file operations
- Test with various IMS file formats

### Pull Requests
- Fork the repository and create a feature branch
- Make atomic commits with clear messages
- Update documentation if needed
- Test thoroughly before submitting

### Testing
- Test with different IMS file structures
- Verify output matches Imaris exports
- Check memory usage with large files
- Validate cross-platform compatibility

## Project Structure
```
ims2tif/
├── ims2tif.py              # Core conversion library
├── simple_converter.py     # Basic interface
├── universal_converter.py  # Flexible paths
├── smart_converter.py      # Imaris-like filtering
├── recursive_converter.py  # Batch processing
├── advanced_converter.py   # Multiple formats
├── requirements.txt        # Dependencies
├── README.md              # Main documentation
└── examples/              # Usage examples
```

Thank you for contributing!
