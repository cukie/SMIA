# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image
import sys
import os


# listdir wrapper that returns the full path of children based on root
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

# returns an image object from the given filepath
def getImage(filepath):
	im = Image.open(filepath)

	return im 

def 


if __name__ == '__main__':

	# first argument - base directory
	base_dir = sys.argv[1]

	# open the file... and perform the given operations for each entry
	count = 1
	for directory in listdir_fullpath(base_dir):
		print "processing directory: " + str(count) 
		count += 1
		for pic in listdir_fullpath(directory):
			pass