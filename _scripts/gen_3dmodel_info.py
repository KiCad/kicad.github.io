"""
This script creates a metadata listing for the entire set of KiCad 3D model libraries.
This is used to create an up-to-date list on the library website,
and also creates JSON data for part searching.
"""

from __future__ import print_function

import argparse
import sys
import os
import json
import glob
from model_list import ModelList
import zipper

"""
Script defines
"""

parser = argparse.ArgumentParser(description="Generate symbol library description")
parser.add_argument('libs', nargs='+', help="List of 3D model libraries (.3dshapes directories)")
parser.add_argument('--output', help='Path to store output markdown files. If blank, no output will be generated')
parser.add_argument('--json', help='Path to store generated JSON file. If blank, no JSON output will be generated')
parser.add_argument('-v', '--verbose', help='Verbosity level', action='count')
parser.add_argument('--download', help='Path to store generated archive files for download. If blank, no archives will be generated')

args = parser.parse_args()

if args.output:
    args.output = os.path.abspath(args.output)

# Default verbosity level
if not args.verbose:
    args.verbose = 0

model_list = []

src_dirs = []

json_data = []

# Read in list of symbol libraries to parse
for lib in args.libs:

    libs = glob.glob(lib)

    for l in libs:
        print(l)
        if os.path.exists(l) and os.path.isdir(l) and l.endswith('.3dshapes'):
            src_dirs.append(l)

def create_output_file(model_list):
    if not args.output:
        return

    if not os.path.exists(args.output):
        ok.mkdirs(args.output)

    output_file = os.path.join(args.output, model_list.name + '.md')

    with open(output_file, 'w') as md_file:
        md_file.write(fp_list.encode_md())

# Iterate through each provided library
for lib_dir in src_dirs:

    lib_name = ''.join(os.path.basename(lib_dir).split('.3dshapes')[:-1])

    print(lib_name)

    if args.verbose > 0:
        print("Encoding library '{l}'".format(l=lib_name))

    # Extract all footprint information
    footprints = []
    files = []

    for f in os.listdir(lib_dir):

        models = ['.step', '.wrl']

        # File types to copy across
        allowed = ['.md', '.txt'] + models

        if not any([f.lower().endswith(x) for x in allowed]):
            continue

        fp_file = os.path.join(lib_dir, f)

        files.append(fp_file)

        # Group models together (e.g. download .step and .wrl in same archive)
        if any([f.lower().endswith(x) for x in models]):
            #TODO
            pass

    if args.download:

        archive_dir = os.path.abspath(os.path.join(args.download, 'packages3d'))

        if not os.path.exists(archive_dir):
            os.mkdirs(archive_dir)

        archive = os.path.join(archive_dir, lib_name + '.7z')

        archive_size = zipper.archive_7z(archive, files)
    else:
        archive_size = None

    # TODO - Extract the name of the library from... somewhere?
    model_list = ModelList(lib_name, 'blank description', archive_size)

    # TODO
    for fp in footprints:
        fp_list.add_footprint(fp)

    fp_list.reorder()

    create_output_file(fp_list)

    if args.json:
        json_data.append(fp_list.encode_json())

if args.json:
    with open(args.json, 'w') as json_file:
        json_output = json.dumps(json_data, separators=(',',':'))
        json_file.write(json_output)
