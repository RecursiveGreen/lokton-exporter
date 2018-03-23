# LOKTON Exporter
LOKTON camera image ('.ss') exporter for FINAL FANTASY XV Windows Edition.

## Requirements
* Python 3.5+
* Pillow (fork of Python Imaging Library)

## Usage
```
lokex.py [-h] [-f {BMP,JPEG,PNG}] [-v] input output

Convert FINAL FANTASY VX '.ss' files to standard image files.

positional arguments:
  input                 Input file/directory with '.ss' files.
  output                Output file/directory to save to.

optional arguments:
  -h, --help            show this help message and exit
  -f {BMP,JPEG,PNG}, --format {BMP,JPEG,PNG}
                        Save as this image format. (Default: JPEG)
  -v, --verbose         Output more information during conversion.
```
