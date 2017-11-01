"""
This script creates a metadata listing for the entire set of KiCad symbol libraries.
This is used to create an up-to-date list on the library website,
and also creates JSON data for part searching.
"""

from __future__ import print_function

import argparse
import sys
import os
import json
import glob
from symbol_list import SymbolList
import zipper
import csv

"""
Script defines
"""

parser = argparse.ArgumentParser(description="Generate symbol library description")
parser.add_argument('libs', nargs='+', help="List of symbol libraries (.lib files)")
parser.add_argument('--schlib', help='Path to schlib scripts (if not already in python path)', action='store')
parser.add_argument('--output', help='Path to store output markdown files. If blank, no output will be generated')
parser.add_argument('--json', help='Path to store generated JSON file. If blank, no JSON output will be generated')
parser.add_argument('--csv', help='Path to .csv file containing symbol library description information')
parser.add_argument('-v', '--verbose', help='Verbosity level', action='count')
parser.add_argument('--download', help='Path to store generated archive files for download. If blank, no archives will be generated')

args = parser.parse_args()

print("Reading symbol libraries")

if args.output:
    args.output = os.path.abspath(args.output)

# Default verbosity level
if not args.verbose:
    args.verbose = 0

if args.schlib:
    sys.path.append(os.path.abspath(args.schlib))

import schlib

symbol_list = []

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
        if os.path.exists(l) and l.endswith('.lib'):
            src_libs.append(l)
            print("Lib:", l)
        else:
            print("Err:", l)

def create_output_file(sym_list):
    if not args.output:
        return

    output_file = os.path.join(args.output, sym_list.name + '.md')

    with open(output_file, 'w') as md_file:
        md_file.write(sym_list.encode_md())

# Iterate through each provided library
for lib_file in src_libs:
    lib_name = ''.join(os.path.basename(lib_file).split('.lib')[:-1])

    lib_path = os.path.dirname(lib_file)

    dcm_file = os.path.join(lib_path, lib_name + '.dcm')

    if args.verbose > 0:
        print("Encoding library '{l}'".format(l=lib_name))

    try:
        library = schlib.SchLib(lib_file)
    except:
        #TODO - Error message!
        continue

    if args.download:
        # Create an archive of this library...
        files = [lib_file, dcm_file]

        archive_dir = os.path.abspath(os.path.join(args.download, 'symbols'))

        if not os.path.exists(archive_dir):
            os.mkdir(archive_dir)

        archive = os.path.join(archive_dir, lib_name + '.7z')

        archive_size = zipper.archive_7z(archive, files)
    else:
        archive_size = None

    # TODO - Extract the name of the library from... somewhere?

    description = descriptions.get(lib_name, '')

    sym_list = SymbolList(lib_name, description, archive_size)

    for c in library.components:
        sym_list.add_component(c, True)

    sym_list.reorder()

    create_output_file(sym_list)

    if args.json:
        json_data.append(sym_list.encode_json())

if args.json:
    with open(args.json, 'w') as json_file:
        json_output = json.dumps(json_data, separators=(',',':'))
        json_file.write(json_output)
