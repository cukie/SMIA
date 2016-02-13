#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukierma
# @Date:   2015-08-30 09:19:30
# @Last Modified by:   cukie
# @Last Modified time: 2016-02-13 08:50:03

# NOTE: This is just a working copy while we do our refactoring

from PIL import Image
import os
import BatchImage
import csv
from collections import OrderedDict
import ntpath
import logging


logger = logging.getLogger(__name__)


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
        # Helps us in determining when to write our headers in our results.
        self.first_dir = True
        # We need a reference to the current BatchImage Object we are
        # processing for, thus, we save it here.
        self.currentBatch = None
        self.result_file = None

    def run(self):
        '''
        Runs a batch of images according to the parameters passed upon initialization of our BatchRunner object.
        '''

        # The main flow here is to loop through each directory creating a list of masks and marker objects respectively.
        # We then create our BatchImage object, perform operations, and write
        # results

        # Open one results file for the whole batch. 'b' flag for other os's 
        self.result_file = open(os.path.join(self.output_path, "results.csv"), 'wb')

        for directory in self._listdir_fullpath(self.base_dir):
            masks, markers = self._masksAndMarkersFromDir(directory)
            batch = BatchImage.BatchImage(
                masks,
                markers,
                self.num_layers,
                self.white_list,
                makeimages=self.output_images,
                makethumbnails=self.output_thumbnails
            )

            # Give the object a reference to our current batch
            self.currentBatch = batch
            self.currentDirectory = directory
            # now we performOps on our current BatchImage instance and save the
            # results.
            results = self._runOperations(self.currentBatch)
            self._saveResults(results, self.currentDirectory)

        # Make sure we clean up after ourselves.
        self.result_file.close()

    def _runOperations(self, batch):
        '''
        Takes a batch and calls performOps on it, aggregating results as we go in an OrderedDict.

        :param BatchImage batch: The batch we want to run
        :return OrderedDict: An OrderedDict of resutls.

        '''

        output_dict = OrderedDict()
        # make sure we always have a directory name
        output_dict['Directory Name'] = self.currentDirectory

        for results in self.currentBatch.PerformOps():
            output_dict = self._mergeDicts(output_dict, results)

        return output_dict

    def _saveResults(self, results_dict, current_directory):
        '''
        We save results based on the output parameters passed into our BatchRunner instance
        '''

        # We must wait to create our write object because we won't know the fieldnames until
        # the BatchImage object gives us results. This is not ideal and we shoul be able to 
        # query the BatchImage object for these fieldnames after initialization of it in the future.

        fieldnames = results_dict.keys()
        writer = csv.DictWriter(self.result_file, fieldnames=fieldnames, dialect='excel')

        if self.first_dir:
	        logger.debug("First write into results.csv. Adding column names: {0}".format(fieldnames))
        	writer.writeheader()
        	self.first_dir = False

        writer.writerow(results_dict)

        if self.output_images:
            # Create a folder for each batch for image results

            save_location = os.path.join(
                self.output_path, ntpath.basename(current_directory) + " images")
            logger.debug("saving output images to: {0}".format(save_location))
            os.makedirs(save_location)

            for image in self.currentBatch.AllResultImages():
                img = image[0]
                name = image[1]

                img.save(os.path.join(save_location, name + '.tif'))
                img.close()

        if self.output_thumbnails:
            # Create a folder for each batch for image results

            save_location = os.path.join(
                self.output_path, ntpath.basename(directory) + " thumbnails")
            logger.debug("saving output thumbnails to: {0}".format(save_location))
            os.makedirs(save_location)

            for image in self.currentBatch.AllResultThumbnails():
                img = image[0]
                name = image[1]
                img.save(os.path.join(save_location, name + '.jpg'))
                img.close()

    def _mergeDicts(self, dict1, dict2):
        """
        Takes two dictionaries and merges them.
        """

        x = dict1.copy()
        x.update(dict2)

        return x

    def _maskOrMarker(self, pic_path):
        """
        A little helper that takes a file prefix and returns "mask" if configuration file deemed it a mask and "marker" if deemed a marker.

        :returns string: "mask" or "marker" respectively according to the type of object we should create. 
        :raise ValueError: an Exception if prefix isn't found in either configuration list.
        """

        # The first item in each entry of our list is the unique identifier for
        # each mask or marker.
        mask_prefixes = [x[0] for x in self.mask_names]
        marker_prefixes = [x[0] for x in self.marker_names]

        # Is it a mask?
        for mask_prefix in mask_prefixes:
            if mask_prefix in pic_path:
                return "mask"

        # Is it a marker?
        for marker_prefix in marker_prefixes:
            if marker_prefix in pic_path:
                return "marker"

        raise ValueError(
            "given marker or mask prefix not found while traversing directory for image: " + pic_path)

    def _picObjInfoFromPath(self, pic_path):
        '''Obtain our name, and threshold form mask_names or marker_names as needed, given a path'''

        # it should be safe to do this because prefixes should be unique no
        # matter what...
        allPicNames = self.mask_names + self.marker_names

        # Once we find the unique prefix in our path, we can return the
        # iformation
        for prefix, name, threshold in allPicNames:
            if prefix in pic_path:
                return name, threshold

    def _getImage(self, pic_path):
        '''wrapper to return an Image object given a path'''
        im = Image.open(pic_path)

        return im

    def _createSinglePicObj(self, pic_path, withNegative=True):
        '''
        Helper that takes a pic path, and creates a mask or marker (depending on whether we've determined the path to be mask or marker

        :param string pic_path: Absolute path of the image we want to create a pic object for
        :param boolean withNegative: If set to true, we'll return two pic objects. One positive and one negative, relative to threshold.
        :returns PicObj: Returns a Mask or Marker object as needed
        '''

        # First get the type of our needed object
        picType = self._maskOrMarker(pic_path)
        name, threshold = self._picObjInfoFromPath(pic_path)
        image = self._getImage(pic_path)
        if withNegative:
            if 'mask' == picType:
                return (BatchImage.Mask(image, name, threshold), BatchImage.Mask(image, name, threshold, makeNegative=True))
            if 'marker' == picType:
                return (BatchImage.Marker(image, name, threshold), BatchImage.Marker(image, name, threshold, makeNegative=True))
        else:
            if 'mask' == picType:
                return (BatchImage.Mask(image, name, threshold),)
            if 'marker' == picType:
                return (BatchImage.Marker(image, name, threshold),)

    def _masksAndMarkersFromDir(self, directory):
        '''
        This helper function loops through our images and creates a list of masks and markers
        in preparation for creating a BatchImage object.
        '''
        masks = []
        markers = []

        for pic in self._listdir_fullpath(directory):
            picObj = self._createSinglePicObj(pic, withNegative=True)

            picType = None
            if isinstance(picObj[0], BatchImage.Mask):
                for mask in picObj:
                    masks.append(mask)

            if isinstance(picObj[0], BatchImage.Marker):
                for marker in picObj:
                    markers.append(marker)

            # TODO: right now we are failing silently here...

        logger.debug("Found {numMasks} masks and {numMarkers} markers in {directory}".format(
            numMasks=len(masks),
            numMarkers=len(markers),
            directory=directory)
        )

        return masks, markers

    def _listdir_fullpath(self, d):
        """
        A wrapper for os.listdir(). Works in the same manner,
        but returns the absolute paths of all children instead
        of the relative paths
        """
        for f in os.listdir(d):
            yield os.path.join(d, f)
