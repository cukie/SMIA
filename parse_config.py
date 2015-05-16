# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/6/15
# (c) All Rights Reserved

import json

"""
This module contains all the logic for parsing a
configuration file (in json format).
"""

def ParseConfig(config_file):
	"""
	Takes in a json filename, opens it, and parses
	the input into a dictionary. The keys in the 
	dictionary are the configuration types and the
	values are those that were inputted by the user.
	As a last step, we perform input validation resulting
	in a boolean value (True if we're all good and False otherwise)
	and a message. If False is returned, all error messages will be
	contained in the message field. 

	Thus the final return value will be a tuple of the following 
	format: (boolean_validation,message,return_dict)
	"""

	configurations = {}

	with open(config_file) as config:
		data = json.load(config)
		# load these values into our globals...
		configurations['base_dir'] = data['base_directory']
		configurations['num_layers']= data['num_pictures']
		configurations['num_masks'] = data['num_masks']
		configurations['num_markers'] = data['num_markers']
		configurations['mask_names'] = data['mask_names']
		configurations['marker_names'] = data['marker_names']
		configurations['mask_opts'] = data['mask_opts']
		configurations['mark_opts'] = data['mark_opts']
		configurations['output_path'] = data['output_to']
		configurations['overlay_white_list'] = data['overlay_white_list']

	# Let's validate our input... Hopefully catch errors early!
	validated,message = TestConfigInput(configurations)

	return (validated,message,configurations)

def TestConfigInput(config_dict):
	"""
	Tests the configuration variables defined in ParseConfig.
	Returns true if good and false if not. A confirm or
	error message is also returned.
	(True/False,message)
	"""


	# Extract our variables from the dictionary so they're
	# Easier to work with

	base_dir = config_dict['base_dir']
	num_layers = config_dict['num_layers']
	num_masks = config_dict['num_masks']
	num_markers = config_dict['num_markers']
	mask_names = config_dict['mask_names']
	marker_names = config_dict['marker_names']
	mask_opts = config_dict['mask_opts']
	mark_opts = config_dict['mark_opts']
	output_path = config_dict['output_path']

	############ Allowable Operation Values ##########
	allowable_mask = ["MASK_INDI","MASK_ALL"]
	allowable_mark = ["MARK_INDI", "MARK_ALL","COLLOC_MARK"]

	# If everything is fine - this list stays empty
	messages = []

	# We're basically just making sure that there's no
	# Default values left here from the config file.
	if base_dir == "full path" or base_dir == None:
		messages.append("Please specify a base directory in the configuration file \n")
		print base_dir
	if num_layers == "number of layers" or num_layers == None or num_layers < 1:
		messages.append("Please specify the number of layers for this run in the configuration file \n")
	if num_masks == "number of masks" or num_masks == None or num_masks < 1:
		messages.append("Please specify the number of masks for this run in the configuration file \n")
	if num_markers == "number of masks" or num_markers == None or num_markers < 1:
		messages.append("Please specify the number of markers for this run in the configuration file \n")
	if len(mask_names) < 1:
		messages.append("Please specify the names and file prefixes of masks for this run in the configuration file \n")
	if len(marker_names) < 1:
		messages.append("Please specify the number of markers for this run in the configuration file \n")

	# all operations must be in our predefined list of
	# acceptable operations. Defined at top of this 
	# function 

	# A mask operation can only be one of two options and not both
	if len(mask_opts) !=1 or mask_opts[0] not in allowable_mask:
		messages.append("Error in mask operation chosen. Please choose exactly one of the two allowable values - see usage notes")

	# We only do one mask or marker operation at a time...
	# Sorry....
	if len(mark_opts) !=1 or mark_opts[0] not in allowable_mark:
		messages.append("Error in marker operation chosen. Please choose exactly one of the three allowable values - see usage notes")

	if output_path == "full output path" or output_path == None:
		messages.append("Please specify an output path in the configuration file\n")

	# If we have error messages
	if len(messages) > 0: 
		# make them pretty and send them off
		return (False, "".join(messages))
	else:
		# every little thing is gonna be alright
		return (True, "Configuration file parsed successfully!")






