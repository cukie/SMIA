# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/4/15
# (c) All Rights Reserved

from PIL import Image

class Mask(object):
	"""
	A mask object is just a Pillow Image object wrapped up 
	in our own concept of a mask. It's a way to logically
	separate the Mask images from the Marker images
	"""
	def __init__(self,img,name):
		self._img=img
		# for now - a mask is just an image with a name
		self.name = name

	# Delegate all of Mask's inner functions to Image
	# e.g. im.__getattr__('size') == im.size if there was no wrapper 
	def __getattr__(self,key):
		if key == '_img':
			raise AttributeError()
		return getattr(self._img,key)

class Marker(object):
	"""
	A marker object is just a Pillow Image object wrapped up 
	in our own concept of a marker. It's a way to logically
	separate the Marker images from the Mask images
	"""
	def __init__(self,img,name):
		self._img=img
		# for now - a mask is just an image with a name
		self.name = name

	# Delegate all of Mask's inner functions to Image
	# e.g. im.__getattr__('size') == im.size if there was no wrapper 
	def __getattr__(self,key):
		if key == '_img':
			raise AttributeError()
		return getattr(self._img,key)


class BatchImage(masks, markers, num_images):
	"""
	A BatchImage object aggregates a set of Mask
	and Marker objects into one clearly defined 
	batch of images. It defines all the operations
	that should be performed on masks and markers.
	"""