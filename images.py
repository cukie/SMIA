# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/29/15
# (c) All Rights Reserved

from PIL import Image

def getImage(filepath):
	im = Image.open(filepath)

	return im 