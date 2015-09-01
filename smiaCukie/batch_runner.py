#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukierma
# @Date:   2015-08-30 09:19:30
# @Last Modified by:   cukie
# @Last Modified time: 2015-08-30 11:03:59

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
		self.first_dir = True # Helps us in determining when to write our headers in our results.
		self.currentBatch = None # We need a reference to the current BatchImage Object we are processing for, thus, we save it here.

	def run(self):
		'''
		Runs a batch of images according to the parameters passed upon initialization of our BatchRunner object.
		'''

		# The main flow here is to loop through each directory creating a list of masks and marker objects respectively.
		# We then create our BatchImage object, perform operations, and write results
		for directory in self._listdir_fullpath(self.base_dir):
			masks, markers = self._masksAndMarkersFromTopDir()
			batch = BI.BatchImage(
				masks,
				markers,
				self.num_layers,
				self.white_list,
				makeimages=self.output_images,
				makethumbnails=self.output_thumbnails
				)

			# Give the object a reference to our current batch
			self.currentBatch = batch

			# now we performOps on our current BatchImage instance and save the results.
			results = self._runOperations()
			self._saveResults(results, directory) 

	def _runOperations(self, batch):
		'''
		Takes a batch and calls performOps on it, aggregating results as we go in an OrderedDict.

		:param BatchImage batch: The batch we want to run
		:return OrderedDict: An OrderedDict of resutls.

		'''

		output_dict = OrderedDict()
		# make sure we always have a directory name
		output_dict['Directory Name'] = directory

		for results in self.currentBatch.performOps():
			output_dict = self._mergeDicts(output_dict,results)

		return output_dict

	def _saveResults(self, results_dict, current_directory):
		'''
		We save results based on the output parameters passed into our BatchRunner instance
		'''
		# open our results file
		f = open(os.path.join(self.output_path,"results.csv"),'wb')
		writer = None

		if self.first_dir:
			fieldnames = list(results_dict.keys())
			writer = csv.DictWriter(f, fieldnames=fieldnames,dialect='excel')
			writer.writeheader()

		writer.writerow(output_dict)
		del output_dict # TODO: Is this needed? Holdover from memory leak search?

		if self.output_images:
			# Create a folder for each batch for image results

			save_location = os.path.join(self.output_path, ntpath.basename(current_directory) + " images")
			os.makedirs(save_location)

			for image in self.currentBatch.AllResultImages():
				img = image[0]
				name = image[1]

				img.save(os.path.join(save_location, name + '.tif'))
				img.close()
				
		if output_thumbnails:
			# Create a folder for each batch for image results

			save_location = os.path.join(self.output_path, ntpath.basename(directory) + " thumbnails")
			os.makedirs(save_location)

			for image in self.currentBatch.AllResultThumbnails():
				img = image[0]
				name = image[1]
				img.save(os.path.join(save_location, name + '.jpg'))
				img.close()

		f.close()

	def mergeDicts(self,dict1,dict2):
		"""
		Takes two dictionaries and merges them.
		"""

		x = dict1.copy()
		x.update(dict2)

		return x

	def _masksAndMarkersFromDir(self, dir):
		'''
		This helper function loops through our images and creates a list of masks and markers
		in preparation for creating a BatchImage object.
		'''
		masks = []
		markers = []

		for pic in self._listdir_fullpath(directory):
			picType, picObj = self._createSinglePicObj(pic, withNegative=True)

			if 'mask' == picType:
				masks.append(picObj[1])
				masks.append(picOBj[2])
			if 'marker' == picType:
				markers.append(picObj[1])
				markers.append(picObj[2])
			#TODO: right now we are failing silently here...

		return masks, markers 


	def _listdir_fullpath(self, d):
		"""
		A wrapper for os.listdir(). Works in the same manner,
		but returns the absolute paths of all children instead
		of the relative paths
		"""
		for f in os.listdir(d):
			yield os.path.join(d,f)






