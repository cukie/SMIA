#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukierma
# @Date:   2015-08-30 09:19:30
# @Last Modified by:   cukie
# @Last Modified time: 2015-08-30 10:03:26

# NOTE: This is just a working copy while we do our refactoring

from   PIL import Image
import sys
import os
import itertools
import BatchImage as BI 
import parse_config as pc 
import time
import csv
from   collections import OrderedDict
import json 
import ntpath
import gc

class BatchRunner():
	'''
	This class encapsulates all the necessary information to run a batch of images.
	It takes in a set of parameters that help define the inputs and outputs of a batch run.

	:param string base_dir: The full path to the top level directory where the images are stored
	:param int num_layers: A count of the total number of layers (mask and marker components) we want to process
	:param int num_masks: A count of the total number of masks we want to process
	:param int num_markers: A count of the total number of markers we want to process
	:param list mask_names: A list of strings corresponding to the names of our mask
	:param list marker_names: A list of strings corresponding to the names of our markers
	:param list white_list: A list of the operations we want to perform. The notion here is 'only do these things and nothing else'
	:param boolean output_images: A flag to denote whether we want to output fullsize images of results
	:param boolean output_thumbnails: A flag to denote whether we want to output thumbnail images of results
	:param string output_path: The absolute path of where we want to save our results

	'''

	def __init__(self, base_dir, num_layers, num_masks, num_markers, mask_names, marker_names, 
					white_list, output_images, output_thumbnails, output_path):
		# Our configuration 
		self.base_dir = base_dir
		self.num_layers = num_layers
		self.num_masks = num_masks
		self.num_markers = num_markers
		self.mask_names = mask_names
		self.marker_names = marker_names
		self.white_list = white_list
		self.output_images = output_images
		self.output_thumbnails = output_thumbnails
		self.output_path = output_path

	def run(self):
		'''
		Runs a batch of images according to the parameters passed upon initialization of our BatchRunner object.
		'''

		# The main flow here is to loop through each directory creating a list of masks and marker objects respectively.
		# We then create our BatchImage object, perform operations, and write results
		masks, markers = self._masksAndMarkersFromTopDir()
		batch = BI.BatchImage(
			masks,
			markers,
			self.num_layers,
			self.white_list,
			makeimages=self.output_images,
			makethumbnails=self.output_thumbnails
			)

	def _masksAndMarkersFromTopDir(self):
		'''
		This helper function loops through our images and creates a list of masks and markers
		in preparation for creating a BatchImage object.
		'''
		masks = []
		markers = []

		for directory in self._listdir_fullpath(self.base_dir):
			for pic in self._listdir_fullpath(directory):
				picType, picObj = self._createSinglePicObj(pic, withNegative=True)

				if picType == 'mask':
					masks.append(picObj[1])
					masks.append(picOBj[2])
				if picType == 'marker':
					markers.append(picObj[1])
					markers.append(picObj[2])
				#TODO: right now we are failing silently here...

		return maks, markers 


	def _listdir_fullpath(self, d):
		"""
		A wrapper for os.listdir(). Works in the same manner,
		but returns the absolute paths of all children instead
		of the relative paths
		"""
		for f in os.listdir(d):
			yield os.path.join(d,f)






