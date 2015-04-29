# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image
import os


# listdir wrapper that returns the full path of children based on root
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

# returns an image object from the given filepath
def getImage(filepath):
	im = Image.open(filepath)

	return im 