# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image
import sys
import os
import itertools
import BatchImage as BI 
import parse_config as pc 
import time
import csv
from collections import OrderedDict
import json 


######## GLOBAL CONFIGURATION VARIABLES ############
base_dir = None
num_layers = None
num_masks = None
num_markers = None
mask_names = []
marker_names = []
mask_opts = []
mark_opts = []
white_list = {}

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

	# open our results file
	f = open(output_path+"/results.csv",'wb')
	writer = None
	# open the file... and perform the given operations for each entry
	count = 0
	for directory in listdir_fullpath(base_dir):
		count += 1
		print "processing directory: " + directory.split(base_dir+"/")[1]
		masks = []
		markers = []
		for pic in listdir_fullpath(directory):
			whichone,prefix,name,threshold = MaskorMarker(pic)
			if whichone == 'mask':
				# let's make a new mask and add it to our list
				masks.append(BI.Mask(getImage(pic),name,threshold))
				masks.append(BI.Mask(getImage(pic),name,threshold,makeNegative=True))
			if whichone == 'marker':
				markers.append(BI.Marker(getImage(pic),name,threshold))
				markers.append(BI.Marker(getImage(pic),name,threshold,makeNegative=True))

		# now let's create a batch image object
		# We pass in num_layers because Batch_image
		# constructor will make sure nothing has gone 
		# wrong... a kind of delegation of error checking
		batch = BI.BatchImage(masks,markers,num_layers,mask_opts,mark_opts,white_list)
		
		output_dict = OrderedDict()
		# make sure we always have a directory name
		output_dict['Directory Name'] = directory

		for results in batch.PerformOps(mask_opts,mark_opts):
			# grab the results tuple and add to output dictionary
			output_dict = MergeDicts(output_dict,results)
		# The first directory, we need to throw the headings in
		# print output_dict
		if count == 1:
			fieldnames = list(output_dict.keys())
			writer = csv.DictWriter(f, fieldnames=fieldnames,dialect='excel')
			writer.writeheader()
		# Fill in our rows
		writer.writerow(output_dict)




def MergeDicts(dict1,dict2):
	"""
	Takes two dictionaries and merges them.
	"""

	x = dict1.copy()
	x.update(dict2)

	return x

def ConfigDictToGlobals(config_dict):
	"""
	Takes a dictionary of key=config_name, value=config_value
	and puts it into our appropriate global variables.
	Note: This subroutine is defined ONLY for its side effects.
	"""
	# We're writing to gloabsl here...
	global base_dir,num_layers,num_masks,num_markers,mask_names,marker_names,mask_opts,mark_opts,output_path, white_list

	base_dir = config_dict['base_dir']
	num_layers = config_dict['num_layers']
	num_masks = config_dict['num_masks']
	num_markers = config_dict['num_markers']
	mask_names = config_dict['mask_names']
	marker_names = config_dict['marker_names']
	mask_opts = config_dict['mask_opts']
	mark_opts = config_dict['mark_opts']
	output_path = config_dict['output_path']
	# We want this as a dictionary for faster lookups
	for sentence in config_dict['overlay_white_list']:
		white_list[sentence] = sentence


output_path = None
def main(config_file):
		# parse the json configuration file
	success,message,config_dict = pc.ParseConfig(config_file)
	if not success:
		print "ERRORS: \n" + message
		sys.exit(1)
	else:
		print message 
	# Set our configuration variables
	ConfigDictToGlobals(config_dict)
	# Here's where the magic happens
	time1 = time.time()
	LoopDirectory()
	with open(output_path+"/used_config.txt",'w') as c:
		json.dump(config_dict,c)
	print time.time() - time1
	# print some success messages
	# ToDo: bundle this up into its own method
	print
	print "You have succesfully procesed:\n" + base_dir
	print
	print "See your results in:\n" + output_path
	print


if __name__ == '__main__':
	main(sys.argv[1])

	# for i in xrange(15):
	# 	time1 = time.time()
	# 	main()
	# 	print time.time() - time1
