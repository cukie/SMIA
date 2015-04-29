# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from __future__ import print_function
from gui import getParentFile
import images as images
# a place to test our modules out!

####### gui.getParentFile() tester #############
filename = getParentFile()
print (filename)

####### listdir_fullpath(d) tester iterate through parent directory tester ########
for directory in images.listdir_fullpath(filename):
	print (directory," ------------ ")
	for pic in images.listdir_fullpath(directory):
		print (pic) 

####### images.getImage tester #################
im = images.getImage("/Users/cukierma/Desktop/APIKEY_amw.tiff")
print(im.format, im.size, im.mode) # see what we got
