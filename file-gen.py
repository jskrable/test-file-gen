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

types = []


def mock(in_rec, out_rec):

    def mock_dict(in_dict):
        obj = {}
        for key in in_dict.keys():
            obj = mock(in_dict, obj)

        return obj

    def mock_list(in_list):
        group = []
        for item in in_list:
            out_item = {}
            out_item = mock(item, out_item)
            group.append(out_item)

        return group

    def type_swap(val):
        if type(val) is str:
            val = False if random.random() > 0.5 else 12345
        elif type(val) is int:
            val = True if random.random() > 0.5 else 'A string value'
        else:
            val = 12345 if random.random() > 0.5 else 'A string value'

        return val

    def val_swap(val):
        if type(val) is str:
            val = ''.join(random.choices(string.ascii_uppercase + string.
            	ascii_lowercase, k=random.randint(1,50)))
        elif type(val) is int:
            val = random.randint(0,(10**10))
        else:
            val = not val

        return val

    def mock_field(val):
        seed = random.random()
        if seed > 0.90:
            val = type_swap(val)
        elif seed < 0.10:
            val = None
        elif 0.50 > seed > 0.40:
            val = val_swap(val)

        return val

    for key, val in in_rec.items():
        if type(val) is dict:
            out_rec[key] = mock_dict(val)
        elif type(val) is list:
            out_rec[key] = mock_list(val)
        else:
            out_rec[key] = mock_field(val)

    return out_rec


infile = './datasets/fin_aid_sample.json'
with open(infile) as f:
    indata = json.load(f)

outdata = []
size = len(indata)

for i, record in enumerate(indata):

    print('processing record', i+1, 'of', size)
    test_rec = {}
    test_rec = mock(record, test_rec)
    outdata.append(test_rec)

outfile = infile[:infile.find('.j')] + '_mock.json'
with open(outfile, 'w') as f:
    json.dump(outdata, f, indent=2)
