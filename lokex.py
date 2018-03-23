#!/usr/bin/env python3
import argparse
import glob
import io
import os
from pathlib import Path

from PIL import Image


# JPEG file headers
# https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format
JPEG_SOI = b'\xff\xd8'      # Start of Image
JPEG_EOI = b'\xff\xd9'      # End of Image

# Image formats list
IMAGE_FORMATS = {
    'BMP': '.bmp',
    'JPEG': '.jpg',
    'PNG': '.png',
}


def generate_output_filename(in_file, out_path, img_format):
    return (out_path / (os.path.splitext(in_file.parts[-1])[0] +
                        IMAGE_FORMATS[img_format]))


def is_input_file(filepath):
    if os.path.exists(filepath):
        return os.path.isfile(filepath)
    raise argparse.ArgumentTypeError('Input file/directory does not exist!')


def is_output_file(filepath):
    return bool(os.path.splitext(filepath)[1]) or not os.path.isdir(filepath)


def get_image_data(filepath):
    with open(filepath, 'rb+') as f:
        data = f.read()

    filename = os.path.split(filepath)[1]
    image_start = data.find(JPEG_SOI)
    image_end = data.find(JPEG_EOI) + 2

    if image_start < 0 or image_end < 0:
        print('WARNING: \'{}\' has no image data! (Skipping)'.format(filename))
        return None
    return data[image_start:image_end]


description = 'Convert FINAL FANTASY VX \'.ss\' files to standard image files.'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('input',
                    help='Input file/directory with \'.ss\' files.')
parser.add_argument('output',
                    help='Output file/directory to save to.')
parser.add_argument('-f', '--format',
                    help='Save as this image format. (Default: JPEG)',
                    choices=list(IMAGE_FORMATS),
                    default='JPEG',
                    type=str.upper)
parser.add_argument('-v', '--verbose',
                    help='Output more information during conversion.',
                    action='store_true')
args = parser.parse_args()

input_path = Path(args.input)
output_path = Path(args.output)

workload = []

if is_input_file(input_path):
    if is_output_file(output_path):
        workload.append({'input_path': input_path,
                         'output_path': output_path,
                         'data': get_image_data(input_path)})
    else:
        new_output = generate_output_filename(input_path,
                                              output_path,
                                              args.format)
        workload.append({'input_path': input_path,
                         'output_path': new_output,
                         'data': get_image_data(input_path)})
else:
    if is_output_file(output_path) or not os.path.exists(output_path):
        raise argparse.ArgumentTypeError('Output directory does not exist!')
    else:
        for f in glob.glob('{}/*.ss'.format(input_path)):
            new_output = generate_output_filename(Path(f),
                                                  output_path,
                                                  args.format)
            workload.append({'input_path': f,
                             'output_path': new_output,
                             'data': get_image_data(f)})

count = 0

for image in workload:
    if image['data']:
        if args.verbose:
            print('{} -> {}'.format(image['input_path'],
                                    image['output_path']))
        if args.format == 'JPEG':
            with open(image['output_path'], 'wb') as f:
                f.write(image['data'])
        else:
            Image.open(io.BytesIO(image['data'])).save(image['output_path'],
                                                       format=args.format)
        count += 1

if args.verbose:
    print('{} image{} successfully converted.'.format(count,
                                                      ('s', '')[count == 1]))
