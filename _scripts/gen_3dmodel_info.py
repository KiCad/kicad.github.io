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
import helpers

"""
Script defines
"""

parser = argparse.ArgumentParser(description="Generate symbol library description")
parser.add_argument('libs', nargs='+', help="List of 3D model libraries (.3dshapes directories)")
parser.add_argument('--output', help='Path to store output markdown files. If blank, no output will be generated')
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
        if os.path.exists(l) and os.path.isdir(l) and l.endswith('.3dshapes'):
            src_dirs.append(l)

def create_output_file(model_list):
    if not args.output:
        return

    if not os.path.exists(args.output):
        ok.makedirs(args.output)

    output_file = os.path.join(args.output, model_list.name + '.md')

    with open(output_file, 'w') as md_file:
        md_file.write(model_list.encode_html())

archive_files = []
model_dirs = []

# Iterate through each provided library
for lib_dir in src_dirs:

    model_groups = {}

    lib_name = ''.join(os.path.basename(lib_dir).split('.3dshapes')[:-1])

    if args.verbose > 0:
        print("Encoding library '{l}'".format(l=lib_name))

    # Extract all footprint information
    footprints = []
    files = []

    for f in os.listdir(lib_dir):

        models = ['.step', '.stp', '.wrl']

        # File types to copy across
        allowed = ['.md', '.txt'] + models

        if not any([f.lower().endswith(x) for x in allowed]):
            continue

        fp_file = os.path.join(lib_dir, f)

        files.append(fp_file)

        # Group models together (e.g. download .step and .wrl in same archive)
        if any([f.lower().endswith(x) for x in models]):

            model = '.'.join(f.split(".")[:-1])

            if model in model_groups:
                model_groups[model].append(f)
            else:
                model_groups[model] = [f]

    if args.download:

        archive_dir = os.path.abspath(os.path.join(args.download, 'packages3d'))

        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        archive_file = lib_name + '.3dshapes.7z'

        archive_files.append(archive_file)

        archive = os.path.join(archive_dir, archive_file)

        archive_size = zipper.archive_7z(archive, files)
    else:
        archive_size = None

    # TODO - Extract the name of the library from... somewhere?
    model_list = ModelList(lib_name, 'blank description', archive_size)

    # Create an individual zip file for each 3D model in this library
    group_archives = []

    model_dirs.append(lib_name + '.3dshapes')

    model_archive_dir = os.path.join(args.download, 'packages3d', lib_name + '.3dshapes')

    for group in model_groups:
        group_files = model_groups[group]
        group_models = [os.path.join(lib_dir, f) for f in group_files]

        lib_archives = []

        model_archive_name = group + '.7z'
        model_archive = os.path.join(model_archive_dir, model_archive_name)

        if args.download:
            group_archive_size = zipper.archive_7z(model_archive, group_models)
        else:
            group_archive_size = None

        group_archives.append(model_archive_name)

        model_list.add_model(group, group_archive_size)

    if args.download:
        helpers.purge_old_archives(model_archive_dir, group_archives)

    create_output_file(model_list)

# Remove old model library archives
if args.download:
    archive_dir = os.path.abspath(os.path.join(args.download, 'packages3d'))
    helpers.purge_old_archives(archive_dir, archive_files)

    helpers.purge_old_folders(archive_dir, model_dirs)