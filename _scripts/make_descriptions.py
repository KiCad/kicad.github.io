"""
This script extracts library description data
from the fp-lib-table and sym-lib-table files

It then generates CSV data that Jekyll can parse.

This means that library descriptions do not have
to be duplicated.
"""

from helpers import read_lib_table
import csv
import os
import argparse

parser = argparse.ArgumentParser(description='Extract library information from a lib-table file')
parser.add_argument('-t', '--table', help='Path to library table file')
parser.add_argument('-c', '--csv', help='Path to .csv output file')

args = parser.parse_args()

entries = read_lib_table(args.table)

with open(args.csv, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['library', 'description'])

    for entry in entries:
        writer.writerow([entry['name'], entry['desc']])