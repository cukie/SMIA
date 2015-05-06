# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/4/15
# (c) All Rights Reserved

from PIL import Image
from sets import Set 
import numpy as np 

class Mask(object):
	"""
	A mask object is just a Pillow Image object wrapped up 
	in our own concept of a mask. It's a way to logically
	separate the Mask images from the Marker images
	"""
	def __init__(self,img,name,threshold):
		self._img=img
		# Close this immediately... We don't need it anymore
		# and having two copies of it KILLS runtime
		img.close()

		self.name = name
		self.threshold = threshold

		# a mask is responsible for keeping track of its 
		# own threshold set of pixels and its 
		# "Not set of pixels" 

		# all our pixels
		self.all_pixels = np.array(self._img)

		self.positive_set = Set()
		self.negative_set = Set()

		# iterate through our pixel map and compare to threshold
		for index, value in np.ndenumerate(self.all_pixels):
			if (value >= self.threshold):
				self.positive_set.add(index)
			else:
				self.negative_set.add(index)


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
	def __init__(self,img,name,threshold):
		self._img=img
		# Close this immediately. DRY
		img.close()

		self.name = name
		self.threshold = threshold

		self.all_pixels = np.array(self._img)

		self.positive_set = Set()
		self.negative_set = Set()

		# iterate through our pixel map and compare to threshold
		for index, value in np.ndenumerate(self.all_pixels):
			if (value >= self.threshold):
				self.positive_set.add(index)
			else:
				self.negative_set.add(index)

	# Delegate all of Marker's inner functions to Image
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
		if num_pics != (len(self.masks) + len(self.markers)):
			raise ValueError("num_pics does not match the cumulative number of masks and markers passed into BatchImage instance.")
		else:
			self.num_pics = num_pics

		# our operations for this batch... 
		self.mask_opts = mask_opts
		self.mark_opts = mark_opts

	def PerformOps(self,mask_opts,marker_opts):
		"""
		Uses the mask_opts and mark_opts to decide which
		operations to perform. Performs them, and returns a
		dictionary of key,value pairs giving with the results.
		Key = Column Heading, Value = Data
		"""

		# This function really just parses the operation lists and chooses which functions to delegate to. It then returns those values. 
		
		# mask operations really only have two options...
		# TODO: this really shouldn't be necessary.. do this earlier.

		maskoperation = mask_opts[0]
		markoperation = marker_opts[0]

		# if we just need singular masks...
		if maskoperation == "MASK_INDI":
			# We have three cases:
			if markoperation == "MARK_INDI":
				pass
			if markoperation == "MARK_ALL":
				pass
			if markoperation == "COLLOC_MARK":
				pass
		else:
			# MASK_ALL things get complicated real fast...
			pass




	def GetOverlayLocations(maskset,markerset):
		"""
		Takes a set of pixel locations and a marker object.
		Returns a set of of pixel values for which the marker
		is under the given maskset.
		"""

		mask = maskset
		marker = markerset

		# set intersection between marker and mask gives us the locations we need 
		overlay = mask.intersection(marker)

		return overlay

	def GetPixelValuesFromCoordinates(setValues,imageObj):
		"""
		Takes a set of coordinate values and returns a dictionary
		of key,value pairs such that each pair is defined as:
		pixellocation,pixelvalue 
		"""
		return_dict = {}
		for location in setValues:
			return_dict[location] = imageObj._img.getpixel(location)