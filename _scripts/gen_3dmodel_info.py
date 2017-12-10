"""
This script creates a metadata listing for the entire set of KiCad 3D model libraries.
This is used to create an up-to-date list on the library website,
and also creates JSON data for part searching.

To reduce the amount of work we have to do,
check the git logs beween <now> and the last time this script was run.
After the script runs, save the current git hash for next time.

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
parser.add_argument('libs', help="Path to 3D model libraries (.3dshapes directories)")
parser.add_argument('--output', help='Path to store output markdown files. If blank, no output will be generated')
parser.add_argument('-v', '--verbose', help='Verbosity level', action='count')
parser.add_argument('--download', help='Path to store generated archive files for download. If blank, no archives will be generated')
parser.add_argument('--hash', help='Path to hash file between git commits')

args = parser.parse_args()

if args.output:
    args.output = os.path.abspath(args.output)

# Default verbosity level
if not args.verbose:
    args.verbose = 0

# Extract hash information
if args.hash:
    git_hash_old = helpers.git_old_hash(args.hash)
    print("Old git hash - " + str(git_hash_old))
else:
    git_hash_old = None
    print("No previous git hash found - rebuilding everything!")

git_hash_new = helpers.git_hash(args.libs)

print("New git hash - " + str(git_hash_new))

model_list = []

src_dirs = []
lib_names = []

json_data = []

folders = os.listdir(args.libs)

for f in folders:
    d = os.path.join(args.libs, f)

    if os.path.isdir(f) and d.endswith('.3dshapes'):
        src_dirs.append(f)
        lib_names.append(f.replace('.3dshapes', ''))

# Extract git diff information
diff = helpers.git_diff(args.libs, git_hash_old)

libs_to_archive = []

# Construct a list of the folders than need to be updated!
if git_hash_old is None:
    libs_to_archive = [x for x in src_dirs]
else:
    for line in diff.split('\n'):

        line = line.strip().split('\t')

        if not len(line) == 2: continue

        op = line[0]
        path = line[1]
        folder = path.split(os.path.sep)[0]

        if not folder.endswith('.3dshapes'): continue

        # If the entire folder has been deleted, continue on!
        if not folder in src_dirs: continue

        if not folder in libs_to_archive:
            libs_to_archive.append(folder)

print("The following 3d shapes folders will be archived:")
for lib in libs_to_archive:
    print("- " + lib)

def create_output_file(model_list):
    if not args.output:
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    output_file = os.path.join(args.output, model_list.name + '.html')

    with open(output_file, 'w') as md_file:
        md_file.write(model_list.encode_html())

archive_files = []
model_dirs = []

# Iterate through each provided library
for lib_dir in libs_to_archive:

    model_groups = {}

    lib_name = ''.join(os.path.basename(lib_dir).split('.3dshapes')[:-1])

    if args.verbose > 0:
        print("Encoding library '{l}'".format(l=lib_name))

    # Extract all footprint information
    footprints = []
    files = []
    models  = []

    for f in os.listdir(lib_dir):

        allowed_models = ['.step', '.stp', '.wrl']

        # File types to copy across
        allowed = ['.md', '.txt'] + allowed_models

        if not any([f.lower().endswith(x) for x in allowed]):
            continue

        filename = os.path.join(lib_dir, f)

        files.append(filename)

        # Group models together (e.g. download .step and .wrl in same archive)
        if any([f.lower().endswith(x) for x in allowed_models]):

            models.append(filename)

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
    model_list = ModelList(lib_name, archive_size)

    for model in models:

        model_name = os.path.split(model)[-1]

        model_list.add_model(model_name, zipper.get_file_size(model))

    model_list.reorder()

    # Create an individual zip file for each 3D model in this library
    #group_archives = []

    #model_dirs.append(lib_name + '.3dshapes')

    #model_archive_dir = os.path.join(args.download, 'packages3d', lib_name + '.3dshapes')

    """
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

    """

    create_output_file(model_list)

# Remove old model library archives
if args.download:
    archive_dir = os.path.abspath(os.path.join(args.download, 'packages3d'))

    valid_archives = [l + '.3dshapes.7z' for l in lib_names]

    helpers.purge_old_archives(archive_dir, valid_archives)

# Remove unwanted html files
if args.output:
    html_files = [x for x in os.listdir(args.output) if x.endswith('.html')]

    for h in html_files:
        name = h.replace('.html', '')

        if not name in lib_names:
            print("Deleting extra file '{x}'".format(x=h))

            f = os.path.join(args.output, h)

            subprocess.call(['rm', h])

if args.hash:
    helpers.write_hash(args.hash, git_hash_new)
