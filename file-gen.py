#!/usr/bin/env python3
# coding: utf-8
"""
file-gen.py
03-05-2019
jack skrable
"""

import json
import random
import math
import sys
import string
import argparse


# Progress bar for cli
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def arg_parser():
    # function to parse arguments sent to CLI
    # setup argument parsing with description and -h method
    parser = argparse.ArgumentParser(
        description='Mocks data in a json file for testing purposes')
    parser.add_argument('-s', '--swap-rate', default=10, type=int, nargs='?',
                        help='the total percent of the file to modify, default 10')
    parser.add_argument('-f', '--file', default='./datasets/sample.json', type=str, nargs='?',
                        help='path of the file to mock')
    parser.add_argument('-r', '--restrict', default=[], type=str, nargs='?',
                        help='list of fields that should be modified only in rare cases')
    # parse args and return
    args = parser.parse_args()
    return args


# Function to mock data for unit testing
# Takes an input dict and an empty output dict
def mock(in_rec, out_rec):

    # Helper function to organize sub-dicts
    def mock_dict(in_dict):
        obj = {}
        for key in in_dict.keys():
            obj = mock(in_dict, obj)

        return obj

    # Helper function to organize sub-lists
    def mock_list(in_list):
        group = []
        for item in in_list:
            out_item = {}
            out_item = mock(item, out_item)
            group.append(out_item)

        return group

    # Helper function to swap data types of child fields
    def type_swap(val):
        if type(val) is str:
            val = False if random.random() > 0.5 else 12345
        elif type(val) is int:
            val = True if random.random() > 0.5 else 'A string value'
        else:
            val = 12345 if random.random() > 0.5 else 'A string value'

        return val

    # Helper function to randomize values of child fields
    def val_swap(val):
        if type(val) is str:
            val = ''.join(random.choices(string.ascii_uppercase + string.
                                         ascii_lowercase, k=random.randint(1, 50)))
        elif type(val) is int:
            val = random.randint(0, (10**10))
        else:
            val = not val

        return val

    # Parent value randomizer helper function
    def mock_field(val):

        swap = math.ceil(SWAP_RATE / 3)
        # Initialize random value for field
        seed = random.random()*100
        # Perform value randomization
        # These ratios can be modified to create larger tests
        if seed > (100 - swap):
            # 10% chance to swap value datatype
            val = type_swap(val)
        elif seed < swap:
            # 10% chance to empty value
            val = None
        elif (math.ceil(swap/2) + 50) > seed > (50 - math.ceil(swap/2)):
            # 10% chance to randomize value within datatype
            val = val_swap(val)

        return val

    # Loop through object k/v pairs
    for key, val in in_rec.items():
        if key in RESTRICT:
            # do nothing
            # print(RESTRICT)
            out_rec[key] = val
        elif type(val) is dict:
            out_rec[key] = mock_dict(val)
        elif type(val) is list:
            out_rec[key] = mock_list(val)
        else:
            out_rec[key] = mock_field(val)

    # Return record with new mocked values
    return out_rec


# MAIN
#####################################################################
args = arg_parser()
SWAP_RATE = args.swap_rate
INFILE = args.file
RESTRICT = args.restrict

print('reading data from', INFILE)
with open(INFILE, encoding='utf-8') as f:
    indata = json.load(f)

outdata = []
size = len(indata)

print('mocking [', SWAP_RATE, '] % of file')
# Loop through list of objects
for i, record in enumerate(indata):

    # Perform mocking on each
    progress(i+1, size, 'of records processed')
    test_rec = {}
    test_rec = mock(record, test_rec)
    outdata.append(test_rec)

# Write new mocked data to output file
outfile = INFILE[:INFILE.find('.j')] + '_mock-' + str(SWAP_RATE) + '.json'
print('\nwriting to', outfile)
with open(outfile, 'w') as f:
    json.dump(outdata, f, indent=2)
