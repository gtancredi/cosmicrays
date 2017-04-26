#!/usr/bin/env python
import argparse
import os
import sys
import logging

'''
Use like:

ls *_raw.fits | xargs -I {} /c/Anaconda3/python.exe linux-tool.py --filepath={}
'''

from common import helpers
from lib import crutils, calc_pos

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', required=True,
                        help='file to parse')

    args = parser.parse_args()
    input_file = os.path.realpath(args.filepath)
    data_ext = helpers.extension_from_filename(input_file)
    pos_ext = helpers.pos_ext_from_data_ext(data_ext)
    pos_input_file = input_file.replace(data_ext, pos_ext)
    img = crutils.load(input_file, pos_input_file)
    _, cr_pixels = crutils.clean_cr(img.data, None, 2)
    crs = crutils.reduce_cr(cr_pixels, img.exposition_duration)
    long, lat, height = calc_pos.calc_pos(img)
    sys.stdout.write("lon: {}, lat: {}, height: {}".format(long, lat, height))