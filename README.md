# Image Processing Toolkit

This repository contains a collection of basic image processing algorithms implemented manually in Python. The focus is on understanding the core logic behind common techniques rather than relying on high-level libraries.

## Project Overview

The project includes the following operations:

| File                 | Description                                         |
|----------------------|-----------------------------------------------------|
| `Grayscale.txt`      | Converts a color image to grayscale.                |
| `Halftone.txt`       | Applies halftoning to simulate grayscale printing.  |
| `FloydSteinberg.txt` | Implements Floyd–Steinberg dithering.               |
| `Canny.txt`          | Performs edge detection using the Canny algorithm.  |
| `dm_graphika.py`     | Python driver script for running and testing the above algorithms. |

All scripts are designed to work with `.png` format images.

## How to Run

To run the application:

1. Make sure your input image is in a supported format (e.g. `.png`, `.jpg`, `.jpeg`).
2. Run the script from the command line and provide the image path as an argument:

```bash
python dm_graphika.py your_image.png