# Test JSON File Generator

This is a command line program to help mock-up JSON files for testing. Clone into a new directory, add a JSON file, and you can mock it up.

There are a few arguments that should be used to maximize benefits:
```
usage: file-gen.py [-h] [-s [SWAP_RATE]] [-f [FILE]] [-r [RESTRICT]]

Mocks data in a json file for testing purposes

optional arguments:
  -h, --help            show this help message and exit
  -s [SWAP_RATE], --swap-rate [SWAP_RATE]
                        the total percent of the file to modify, default 10
  -f [FILE], --file [FILE]
                        path of the file to mock
  -r [RESTRICT], --restrict [RESTRICT]
                        list of fields that should be modified only in rare
                        cases
```                        

Happy testing
