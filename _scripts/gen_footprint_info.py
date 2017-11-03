"""
This script creates a metadata listing for the entire set of KiCad footprint libraries.
This is used to create an up-to-date list on the library website,
and also creates JSON data for part searching.
"""

from __future__ import print_function

import argparse
import sys
import os
import json
import glob
from fp_list import FootprintList
import zipper
import helpers

"""
Script defines
"""

parser = argparse.ArgumentParser(description="Generate symbol library description")
parser.add_argument('libs', nargs='+', help="List of footprint libraries (.pretty directories)")
parser.add_argument('--script', help='Path to kicad utils scripts (if not already in python path)', action='store')
parser.add_argument('--output', help='Path to store output markdown files. If blank, no output will be generated')
parser.add_argument('--json', help='Path to store generated JSON file. If blank, no JSON output will be generated')
parser.add_argument('--csv', help='Path to .csv file containing footprint library description information')
parser.add_argument('-v', '--verbose', help='Verbosity level', action='count')
parser.add_argument('--download', help='Path to store generated archive files for download. If blank, no archives will be generated')

args = parser.parse_args()

if args.output:
    args.output = os.path.abspath(args.output)

# Default verbosity level
if not args.verbose:
    args.verbose = 0

if args.script:
    includes = ['common', 'pcb']

    for inc in includes:
        inc = os.path.abspath(os.path.join(args.script, inc))

        sys.path.append(inc)

# It it assumed by this point that utils/pcb is included
from kicad_mod import KicadMod

fp_list = []

src_libs = []

json_data = []

# Read library descriptions
descriptions = {}

if args.csv:
    with open(args.csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            lib_name = row['Library']
            lib_desc = row['Description']
            descriptions[lib_name] = lib_desc

# Read in list of symbol libraries to parse
for lib in args.libs:

    libs = glob.glob(lib)

    for l in libs:
        if os.path.exists(l) and os.path.isdir(l) and l.endswith('.pretty'):
            src_libs.append(l)

def create_output_file(fp_list):
    if not args.output:
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    output_file = os.path.join(args.output, fp_list.name + '.html')

    with open(output_file, 'w') as html_file:
        html_file.write(fp_list.encode_html())

lib_names = []

# Iterate through each provided library
for lib_dir in src_libs:

    lib_name = ''.join(os.path.basename(lib_dir).split('.pretty')[:-1])

    lib_names.append(lib_name)

    if args.verbose > 0:
        print("Encoding library '{l}'".format(l=lib_name))

    # Extract all footprint information
    footprints = []
    files = []

    for f in os.listdir(lib_dir):

        # File types to copy across
        allowed = ['.md', '.txt', '.kicad_mod']

        if not any([f.lower().endswith(x) for x in allowed]):
            continue

        fp_file = os.path.join(lib_dir, f)

        files.append(fp_file)

        if f.endswith('.kicad_mod'):
            try:
                fp = KicadMod(fp_file)
                footprints.append(fp)
            except:
                print("Error loading {fp}".format(fp=fp_file))
                # Skip to the next one
                continue

    if args.download:

        archive_dir = os.path.abspath(os.path.join(args.download, 'footprints'))

        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        archive = os.path.join(archive_dir, lib_name + '.7z')

        archive_size = zipper.archive_7z(archive, files)
    else:
        archive_size = None

    description = descriptions.get(lib_name, '')
    fp_list = FootprintList(lib_name, description, archive_size)

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

# Remove old symbol library archives
if args.download:
    archive_dir = os.path.abspath(os.path.join(args.download, 'footprints'))
    helpers.purge_old_archives(archive_dir, lib_names)
