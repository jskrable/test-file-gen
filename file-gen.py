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
import string

# Globals 
# Total percent of file that will be modified
SWAP_RATE = 30
# Fields that should be modifed very rarely
HOLD = ['univId']
# File to mock
INFILE = './datasets/fin_aid_base.json'


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
        if type(val) is dict:
            out_rec[key] = mock_dict(val)
        elif type(val) is list:
            out_rec[key] = mock_list(val)
        # Smaller change percentage for primary key
        elif key in HOLD:
            if random.random() > 0.96:
                out_rec[key] = mock_field(val)
        else:
            out_rec[key] = mock_field(val)

    # Return record with new mocked values
    return out_rec


# MAIN
#####################################################################

with open(INFILE, encoding='utf-8') as f:
    indata = json.load(f)

outdata = []
size = len(indata)

# Loop through list of objects
for i, record in enumerate(indata):

    # Perform mocking on each
    print('processing record', i+1, 'of', size)
    test_rec = {}
    test_rec = mock(record, test_rec)
    outdata.append(test_rec)

# Write new mocked data to output file
outfile = INFILE[:INFILE.find('.j')] + '_mock.json'
print('writing to',outfile)
with open(outfile, 'w') as f:
    json.dump(outdata, f, indent=2)
