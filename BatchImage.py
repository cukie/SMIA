# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/4/15
# (c) All Rights Reserved

from PIL import Image
import operator
import numpy as np 
import itertools
import sys
from sets import Set


def IndicesByThreshold(pixel_list,threshold,op):
	"""
	Returns a numpy array of indices such that each 
	item in the array is an index of the input list
	as identified by the op parameter.

	E.g. if you want all indices where the pixel value
	is greater than the threshold, pass in 'operator.gt'
	"""

	pixel_arr = np.asarray(pixel_list)
	indices = np.argwhere(op(pixel_arr,threshold))
	return indices 


def GetValuesFromOverlay(mask_indices,marker):
	"""
	Reveals the values of a marker underneath a mask.
	Takes in a numpy array of valid indices and returns
	a numpy array of marker values at those indices. 
	"""

	# First we need just those indices that satisfy both thresholds
	indices = GetIntersection(mask_indices,marker.masked_indices)
	# Also grab an array of all marker pixel values
	marker_pixels = np.asarray(marker.pixel_list)

	# give me the values of marker_pixels under our indices
	values = marker_pixels[indices.flatten()]

	return values

def GetIndicesFromOverlay(mask_indices,marker):
	"""
	returns indices from an overlay.
	Logic is simple - but semantically this makes 
	more sense
	"""

	return mask_indices

def GetOverlayName(mask_name,marker_name):
	return marker_name + " under " + mask_name

def GetIntersection(arr1,arr2):
	"""
	given two arrays, returns an array with the GetArrIntersection
	of values
	"""

	#TODO: check "true" flag... this could speed things up.
	return np.intersect1d(arr1,arr2)

class Mask(object):
	"""
	A mask object is just a Pillow Image object wrapped up 
	in our own concept of a mask. It's a way to logically
	separate the Mask images from the Marker images.

	Note: The mageNegative flag, when set to true will create 
	another Mask object with the inverse mask of the first. 
	"""
	def __init__(self,img,name,threshold,makeNegative=False):
		#TODO: represent negative images with inverse pixels...
		self._img = img
		self.threshold = threshold 
		self.pixel_list = list(img.getdata())
		self.name = None 
		# check our flag to see get the right operator and name
		op = None
		if makeNegative:
			self.name = "NOT" + name
			op = operator.lt
		else:
			self.name = name
			op = operator.ge 			

		self.masked_indices = IndicesByThreshold(self.pixel_list, self.threshold,op)

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
	separate the Marker images from the Mask images.
	"""
	def __init__(self,img,name,threshold,makeNegative=False):
		self._img = img
		op = None
		if makeNegative:
			self.name = "NOT"+name
			op = operator.lt
		else:
			self.name = name
			op = operator.ge
		self.threshold = threshold		
		self.pixel_list = list(img.getdata())
		self.masked_indices = IndicesByThreshold(self.pixel_list,self.threshold,op)


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

	def __init__(self, mask_list, mark_list, num_pics, mask_opts,mark_opts,white_list):

		# as we iterate here - raise exception if these aren't masks
		# and markers respectively
		self.white_list = {}
		self.mask_white_list = {}

		for key in white_list:
			key_list = key.replace(',','')
			key_list = key_list.split()
			tupname = tuple(sorted(key_list))
			self.white_list[tupname] = tupname

		for key in white_list:
			# Grab the list of masks which comes after under
			mask = key.split('under')[1]
			mask = ''.join(mask)
			mask = mask.replace(',','')
			mask = tuple(sorted(mask.split()))
			self.mask_white_list[mask] = mask

		self.masks = []
		for mask in mask_list:
			if type(mask) is not Mask:
				raise ValueError("all values is mask_list parameter must be masks. " + type(mask) + " passed as part of list.")
			else:
				self.masks.append(mask)
		
		# and let's do the same with our markers
		self.markers = []
		for marker in mark_list:
			if type(marker) is not Marker:
				raise ValueError("all values is mark_list parameter must be markers. " + type(marker) + " passed as part of list.")
			else:
				self.markers.append(marker)

		# Let's just make sure everything is here and consistent
		# before we assign each value
		if num_pics != (len(self.masks) / 2 + len(self.markers)/2):
			raise ValueError("num_pics does not match the cumulative number of masks and markers passed into BatchImage instance.")
		else:
			self.num_pics = num_pics

		# our operations for this batch... We can only have one operation for mask and marker...
		self.mask_opts = mask_opts[0]
		self.mark_opts = mark_opts[0]


		# Let's keep a record of the total number of pixels in an image
		self.size = self.masks[0]._img.size
		self.mode = self.masks[0]._img.mode
		self.num_pixels = self.size[0] * self.size[1]

		self.mask_tuples = []
		self.colloc_tuples = []
		
		self.CreateAllColloc()

	def CreateAllMasks(self):
		"""
		A helper that takes a list of masks and creates the powerset of them
		minus the useless ones... Where useless is defined as a mask with 
		itself and NOT itself in the same mask...

		NOTE: does not include collocalized markers in masks 
		"""
		
		self.mask_tuples = self.MasksFromList(self.masks,self.num_pics)

	def CreateAllColloc(self):
		"""
		Creates all masks including those possibilities of 
		collocalized masks.
		"""
		self.colloc_tuples = self.MasksFromList(self.markers + self.masks,self.num_pics)

	def MasksFromList(self,mask_list,combination_max):
		"""
		Given a list of Mask or Marker objects
		returns a list of all combinations of masks
		in the form of a tuple. (mask_loc,name)
		"""
		mask_tuples = []
		count = 0
		for lim in xrange(1,combination_max+1):
				for item in itertools.combinations(mask_list,lim):
					
					# Create our list of names
					names = [x.name for x in item]
					# If this combination is not useless...
					if not self.IsUseless(names):
						count += 1
						sys.stdout.write("\rProcessing Mask %i" % count)
						sys.stdout.flush()
						# our original mask will have all indices in it
						output_mask = np.arange(0,self.num_pixels)
						for mask in item:
							# like a cumsum of intersections...
							output_mask = GetIntersection(output_mask,mask.masked_indices.flatten())
						names = ', '.join(names)
						# print output_mask.size
						mask_tuples.append((output_mask, names))
		sys.stdout.write("\n")

		return mask_tuples



	def PerformOps(self,mask_opts,marker_opts):
		"""
		Uses the mask_opts and mark_opts to decide which
		operations to perform. Performs them, and returns a
		dictionary of key,value pairs giving with the results.
		Key = Column Heading, Value = Data
		"""

		count = 0 
		# We are basically going to take the entire mask_tuples 
		# structure and overlay it with every marker. 
		for combination in itertools.product(self.colloc_tuples,self.markers):
			count+=1
			name = GetOverlayName(combination[0][1], combination[1].name)
			# print name
			name_list = name.replace(',','')
			name_list = name_list.split()
			if self.InWhiteList(name_list):
				values = GetValuesFromOverlay(combination[0][0],combination[1])
				indices = GetIndicesFromOverlay(combination[0][0],combination[1])
				# print name
				# print values.mean()
				yield name


	def _Calculations(self,values,indices,overlay_name):
		"""
		returns a dictionary of keys and values where
		key is operation name and value is the result of 
		the named operation.

		E.g. calculations['mean'] = mean_value
		"""
	def IsUseless(self,names):
		"""
		takes a proposed mask name and tells you if it's useless.
		Useless is defined as a mask with itself and not itself 
		within one name.

		Extended to also define Useless as a mask combination
		not in our white list. 
		"""

		tupnames = tuple(sorted(names))
		if tupnames in self.mask_white_list:
			return False
		else:
			return True

	def InWhiteList(self,names):
		"""
		Returns true if a name is in the white list
		"""
		tupnames = tuple(sorted(names))
		# print tupnames
		if tupnames in self.white_list:
			return True
		else:
			return False 


