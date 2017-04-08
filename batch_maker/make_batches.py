# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/18/15
# (c) All Rights Reserved


"""
A command line tool that allows a user to convert
a directory of raw images into "batches" for use in
the SMIA-CUKIE application.

Parsing used here is specific to the Cukierman lab
use cases, but could be used as an example of the proper 
format to feed into the SMIA-CUKIE application (and how
to automate this process).
"""


import os
import sys
import shutil
from sets import Set
from PIL import Image 

def IsolateUnique(filename):
	part1 = filename.split('[')[1]
	part2 = part1.split(']')[0]

	return part2 

def main(base_directory):
	# Grab the path to our top level directory
	base_dir = base_directory
	blank_image = None

	parent_dir = os.path.join(os.path.dirname(base_dir), os.pardir)
	print parent_dir

	all_files = os.listdir(base_dir)

	# a set of all unique filenames
	file_set = Set()

	firstone = True 

	print "isolating batches..."
	# Get all unique batch names
	for filename in all_files:
		if filename.endswith('.tif') or filename.endswith('.tiff'):
			# if this is the first image we are seeing, let's get our dimensions
			if firstone: 
				img = Image.open(os.path.join(base_dir,filename))
				size = img.size
				listlen = size[0]*size[1]
				mode = img.mode
				img.close()
				del img 
				firstone=False

				# now let's make one blank image...
				blank_image = Image.new(mode,size)
				imglist = [255]*listlen
				blank_image.putdata(imglist)
				blank_image.save(os.path.join(parent_dir,'blanktemp.tif'))
				blank_image.close()
				del blank_image
				del imglist

			isolated = IsolateUnique(filename)
			file_set.add(isolated)

	if base_dir[-1] == os.sep:
		base_dir = base_dir[:-1]
	new_dir = os.path.join(parent_dir,os.path.basename(base_dir) + ' Batches')
	print base_dir
	print new_dir
	os.makedirs(new_dir)

	print "making batch folders..."
	# Create a folder for each unique batch name
	for filename in file_set:
		os.makedirs(os.path.join(new_dir,filename))

	print "copying images into batch folders..."
	# Now iterate through the top level directory again, copying to respective files
	count = 1
	for filename in all_files:
		sys.stdout.write("\r Percent Completed: %f" % (float(count)/len(all_files) * 100))
		sys.stdout.flush()
		count+=1

		first=True
		# we don't want to copy the im3 files...
		if filename.endswith('.tif') or filename.endswith('.tiff'):
			isolated = IsolateUnique(filename)
			if first:
				# copy our original blank image into this directory
				shutil.copy(os.path.join(parent_dir,'blanktemp.tif'), os.path.join(new_dir,isolated,'BLANK.tif'))
				first=False
			shutil.copy(os.path.join(base_dir,filename), os.path.join(new_dir,isolated,filename))

	print "Success! Batches Made."


if __name__ == '__main__':
	main(sys.argv[1])
