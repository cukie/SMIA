# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/2/15
# (c) All Rights Reserved

import json
import sys
from pprint import pprint
import itertools # iterate key value pairs in dict

"""
A tester for our make_config.py file. Attempts to read in 
json data from a file passed to it from the command line. 
"""

json_test = sys.argv[1]

with open(json_test) as data_file:    
    data = json.load(data_file)
    for key,value in data.iteritems():
    	print (key,value)