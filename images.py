# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image
import sys
import os
import itertools
import json
import BatchImage as BI 
import time


######## GLOBAL CONFIGURATION VARIABLES ############
base_dir = None
num_layers = None
num_masks = None
num_markers = None
mask_names = []
marker_names = []
mask_opts = []
mark_opts = []

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
	global base_dir,num_layers,num_markers,num_masks,mask_names,marker_names,output_path, operations

	with open(config_file) as config:
		data = json.load(config)
		# load these values into our globals...
		base_dir = data['base_directory']
		num_layers = data['num_pictures']
		num_masks = data['num_masks']
		num_markers = data['num_markers']
		mask_names = data['mask_names']
		marker_names = data['marker_names']
		mask_opts = data['mask_opts']
		mark_opts = data['mark_opts']
		output_path = data['output_to']

def TestConfigInput():
	"""
	Tests the global variables defined in ParseConfig.
	Returns true if good and false if not. A confirm or
	error message is also returned.
	(True/False,message)
	"""

	############ Allowable Operation Values ##########
	allowable_mask = ["MASK_INDI","MASK_ALL"]
	allowable_mark = ["MARK_INDI", "MARK_ALL","COLLOC_MARK"]

	############ Input Validators ###################

	# We're basically just making sure that there's no
	# Default values left here from the config file.

	# If everything is fine - this list stays empty
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

	# all operations must be in our predefined list of
	# acceptable operations. Defined at top of this 
	# function 
	for operation in mask_opts:
		if operation not in allowable_mask:
			messages.append("Error in mask operation chosen - please see usage notes")
	for operation in mark_opts:
		if operation not in allowable_mark:
			messages.append("Error in marker operation chosen - please see usage notes")


	if output_path == "full output path" or output_path == None:
		messages.append("Please specify an output path in the configuration file\n")

	# If we have error messages
	if len(messages) > 0: 
		# make them pretty and send them off
		return (False, "".join(messages))
	else:
		# every little thing is gonna be alright
		return (True, "Configuration file parsed successfully!")

def MaskorMarker(pic_path):
	"""
	A little helper that takes a file prefix and 
	returns "mask" if configuration file deemed it a 
	mask and "marker" if deemed a marker.
	Raises an Exception if prefix isn't found in either
	configuration list.
	"""

	mask_prefixes = [x[0] for x in mask_names]
	marker_prefixes = [x[0] for x in marker_names]

	for mask_prefix,mask_info in zip(mask_prefixes,mask_names):
		if mask_prefix in pic_path:
			prefix,name,treshold = mask_info
			return ("mask",prefix,name,treshold)
	for marker_prefix,marker_info in zip(marker_prefixes,marker_names):
		if marker_prefix in pic_path:
			prefix,name,treshold = marker_info
			return ("marker",prefix,name,treshold)

	raise ValueError("given marker or mask prefix not found while traversing directory")


def LoopDirectory():
	"""
	Iterates through the base directory accessing each
	batch of images at a time, creating a BatchImage 
	object. Then, performs the functions identified
	in toPerform on each batch. See documentation
	for the options for toPerform.
	"""

	# open the file... and perform the given operations for each entry
	count = 1
	for directory in listdir_fullpath(base_dir):
		print "processing directory: " + str(count) 
		count += 1
		masks = []
		markers = []
		for pic in listdir_fullpath(directory):
			whichone,prefix,name,threshold = MaskorMarker(pic)
			if whichone == 'mask':
				# let's make a new mask and add it to our list
				masks.append(BI.Mask(getImage(pic),name,threshold))
			if whichone == 'marker':
				markers.append(BI.Marker(getImage(pic),name,threshold))

		# now let's create a batch image object
		# We pass in num_layers because Batch_image
		# constructor will make sure nothing has gone 
		# wrong... a kind of delegation
		batch = BI.BatchImage(masks,markers,num_layers,mask_opts,mark_opts)
		batch.PerformOps(mask_opts,mark_opts)

		# print "Masks: "
		# for mask in batch.masks:
		# 	print mask.name
		# print "Markers: "
		# for marker in batch.markers:
		# 	print marker.name

def main():
		# parse the json configuration file
	config_file = sys.argv[1]
	ParseConfig(config_file)
	success, message = TestConfigInput()
	if not success:
		print "ERRORS: \n" + message
		sys.exit(1)
	else:
		print message 

	# Here's where the magic happens
	LoopDirectory()

	# print some success messages
	# ToDo: bundle this up into its own method
	print
	print "You have succesfully procesed:\n" + base_dir
	print
	print "See your results in:\n" + output_path
	print


if __name__ == '__main__':
	main()
	# for i in xrange(15):
	# 	time1 = time.time()
	# 	main()
	# 	print time.time() - time1
