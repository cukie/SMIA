# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image
import sys
import os
import itertools
import json


######## GLOBAL CONFIGURATION VARIABLES ############
base_dir = None
num_layers = None
num_masks = None
num_markers = None
mask_names = {}
marker_names = {}

output_path = None

# listdir wrapper that returns the full path of children based on root
def listdir_fullpath(d):
	"""
	A wrapper for os.listdir(). Works in the same manner,
	but returns the absolute paths of all children instead
	of the relative paths
	"""
	return [os.path.join(d, f) for f in os.listdir(d)]

# returns an image object from the given filepath
def getImage(filepath):
	"""
	Given a filepath, returns an Image object of
	the image in that filepath
	"""
	im = Image.open(filepath)

	return im 

def ParseConfig(config_file):
	"""
	Takes in a json filename, opens it, and parses
	the input into our global config variables 
	"""
	global base_dir,num_layers,num_markers,num_masks,mask_names,marker_names,output_path

	with open(config_file) as config:
		data = json.load(config)
		# load these values into our globals...
		base_dir = data['base_directory']
		num_layers = data['num_pictures']
		num_masks = data['num_masks']
		num_markers = data['num_markers']
		mask_names = data['mask_names']
		marker_names = data['marker_names']
		output_path = data['output_to']

def TestConfigInput():
	"""
	Tests the global variables defined in ParseConfig.
	Returns true if good and false if not. A confirm or
	error message is also returned.
	(True/False,message)
	"""
	# We're basically just making sure that there's no
	# Default values left here from the config file.

	messages = []
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
	if output_path == "full output path" or output_path == None:
		messages.append("Please specify an output path in the configuration file\n")

	if len(messages) > 0:
		return (False, "".join(messages))
	else:
		return (True, "Configuration file parsed successfully!")

def LoopDirectory(toPerform):
	"""
	Iterates through the base directory accessing each
	batch of images at a time, creating a BatchImage 
	object. Then, performs the functions identified
	in toPerform on each batch. See documentation
	for the options for toPerform.
	"""

if __name__ == '__main__':

	# parse the json configuration file
	config_file = sys.argv[1]
	ParseConfig(config_file)
	success, message = TestConfigInput()
	if not success:
		print "ERRORS: \n" + message
		sys.exit(1)
	else:
		print message 


	# open the file... and perform the given operations for each entry
	# count = 1
	# for directory in listdir_fullpath(base_dir):
	# 	print "processing directory: " + str(count) 
	# 	count += 1
	# 	for pic in listdir_fullpath(directory):
	# 		pass