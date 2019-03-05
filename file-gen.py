#!/usr/bin/env python3
# coding: utf-8
"""
file-gen.py
03-05-2019
jack skrable
"""

import json
import random
import string


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

    # Parent value randomizer helper function 
    def mock_field(val):

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
	            	ascii_lowercase, k=random.randint(1,50)))
	        elif type(val) is int:
	            val = random.randint(0,(10**10))
	        else:
	            val = not val

	        return val

	    # Initialize random value for field
        seed = random.random()
        # Perform value randomization
        # These ratios can be modified to create larger tests
        if seed > 0.90:
        	# 10% chance to swap value datatype
            val = type_swap(val)
        elif seed < 0.10:
        	# 10% chance to empty value
            val = None
        elif 0.50 > seed > 0.40:
        	# 10% chance to randomize value within datatype
            val = val_swap(val)

        return val

    # Loop through object k/v pairs
    for key, val in in_rec.items():
        if type(val) is dict:
            out_rec[key] = mock_dict(val)
        elif type(val) is list:
            out_rec[key] = mock_list(val)
        else:
            out_rec[key] = mock_field(val)

    # Return record with new mocked values
    return out_rec

# MAIN
#####################################################################
infile = './datasets/fin_aid_sample.json'
with open(infile) as f:
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
outfile = infile[:infile.find('.j')] + '_mock.json'
with open(outfile, 'w') as f:
    json.dump(outdata, f, indent=2)
