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


class BatchImage():
	"""
	A BatchImage object aggregates a set of Mask
	and Marker objects into one clearly defined 
	batch of images. It defines all the operations
	that should be performed on masks and markers.
	"""

	def __init__(self, mask_list, mark_list, num_pics, mask_opts,mark_opts):

		# as we iterate here - raise exception if these aren't masks
		# and markers respectively
		self.masks = []
		for mask in mask_list:
			if type(mask) is not Mask:
				raise ValueError("all values is mask_list parameter must be masks. " + type(mask) + " passed as part of list.")
			else:
				self.masks.append(mask)
		self.markers = []

		# and let's do the same with our markers
		for marker in mark_list:
			if type(marker) is not Marker:
				raise ValueError("all values is mark_list parameter must be markers. " + type(marker) + " passed as part of list.")
			else:
				self.markers.append(marker)

		# Let's just make sure everything is here and consistent
		# before we assign each value
		if num_pics != (len(masks) + len(markers)):
			raise ValueError("num_pics does not match the cumulative number of masks and markers passed into BatchImage instance.")
		else:
			self.num_pics = num_pics

		# our operations for this batch... 
		self.mask_opts = mask_opts
		self.mark_opts = mark_opts

		




