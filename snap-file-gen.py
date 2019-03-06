# snap-file-gen.py
# 03-05-2019
# jack skrable
# NOTE: need a mapper immediately preceding the script snap with one
# line, JSON.stringify($) -> $doc

# Import the interface required by the Script snap.
from com.snaplogic.scripting.language import ScriptHook
import java.util
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

class TransformScript(ScriptHook):
    def __init__(self, input, output, error, log):
        self.input = input
        self.output = output
        self.error = error
        self.log = log

    # Called once when the pipeline is started
    def execute(self):
        self.log.info("Executing Transform script")
        while self.input.hasNext():
            try:
                # Read the next document
                in_doc = self.input.next()
                in_rec = json.loads(in_doc['doc'])

                test_rec = {}
                test_rec = mock(in_rec, test_rec)

                out_doc = java.util.HashMap()
                out_doc['output'] = test_rec

                self.output.write(out_doc)
            except Exception as e:
                errWrapper = {
                    'errMsg' : str(e.args)
                }
                self.log.error("Error in python script")
                self.error.write(errWrapper)

        self.log.info("Finished executing the Transform script")

# The Script Snap will look for a ScriptHook object in the "hook"
# variable.  The snap will then call the hook's "execute" method.
hook = TransformScript(input, output, error, log)