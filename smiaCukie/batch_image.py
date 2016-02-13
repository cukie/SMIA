# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/4/15
# (c) All Rights Reserved

"""
The BatchImage module defines Mask Objects and Marker Objects.
Most importantly it defines BatchImage Objects which are aggregations
of masks and markers (maybe a tiff stack...).

Additionally, it defines the functions used to analyze the overlaying of
masks and markers. A typical pseudo-code usage definition is as follows:
        Create mask objects
        Create marker objects
        Create BatchImage object from Mask and Marker Objects
        Call PerformOps() to get an OrderedDict of results for each overlay
            defined in your white_list
"""

import operator
import numpy as np
from collections import OrderedDict
from PIL import Image
import logging


logger = logging.getLogger(__name__)


class Mask(object):
    """
    A mask object is just a Pillow Image object wrapped up
    in our own concept of a mask. It's a way to logically
    separate the Mask images from the Marker images.

    Note: The mageNegative flag, when set to true will create
    another Mask object with the inverse mask of the first.
    """

    def __init__(self, img, name, threshold, makeNegative=False):
        # TODO: represent negative images with inverse pixels...
        self._img = img
        self.threshold = threshold
        self.pixel_list = list(img.getdata())

        if makeNegative:
            self.name = "NOT" + name
            op = operator.lt
        else:
            self.name = name
            op = operator.ge

        self.masked_indices = IndicesByThreshold(
            self.pixel_list, self.threshold, op)

    # Delegate all of Mask's inner functions to Image
    # e.g. im.__getattr__('size') == im.size if there was no wrapper
    def __getattr__(self, key):
        if key == '_img':
            raise AttributeError()
        return getattr(self._img, key)


class Marker(object):
    """
    A marker object is just a Pillow Image object wrapped up 
    in our own concept of a marker. It's a way to logically
    separate the Marker images from the Mask images.
    """

    def __init__(self, img, name, threshold, makeNegative=False):
        self._img = img
        op = None
        if makeNegative:
            self.name = "NOT" + name
            op = operator.lt
        else:
            self.name = name
            op = operator.ge
        self.threshold = threshold
        self.pixel_list = list(img.getdata())
        self.masked_indices = IndicesByThreshold(
            self.pixel_list, self.threshold, op)

    # Delegate all of Marker's inner functions to Image
    # e.g. im.__getattr__('size') == im.size if there was no wrapper
    def __getattr__(self, key):
        if key == '_img':
            raise AttributeError()
        return getattr(self._img, key)


class BatchImage():
    """
    A BatchImage object aggregates a set of Mask
    and Marker objects into one clearly defined
    batch of images. It defines all the operations
    that should be performed on masks and markers.
    """

    def __init__(self, mask_list, mark_list, num_pics, white_list, makeimages=False, makethumbnails=False):

        # A couple of boolean values for later
        self.makethumbnails = makethumbnails
        self.makeimages = makeimages
        # TODO: take a white_list in: emphasis on list.. not dict
        self.white_list = [
            operation.replace(" ", "") for operation in white_list]

        # We validate out mask and marker lists before we accept them.
        self.masks = []
        for mask in mask_list:
            if type(mask) is not Mask:
                raise ValueError(
                    "all values is mask_list parameter must be masks. " + type(mask) + " passed as part of list.")
            else:
                self.masks.append(mask)

        self.markers = []
        for marker in mark_list:
            if type(marker) is not Marker:
                raise ValueError(
                    "all values is mark_list parameter must be markers. " + type(marker) + " passed as part of list.")
            else:
                self.markers.append(marker)

        # sanity check. really unecessary... we should be able to deduce this
        # ourselves. not trust the user.
        if num_pics != (len(self.masks) / 2 + len(self.markers) / 2):
            raise ValueError(
                "num_pics does not match the cumulative number of masks and markers passed into BatchImage instance.")
        else:
            self.num_pics = num_pics

        # We keep a record of some image attributes handy.
        # Assumption: these will be the same across all images.
        self.size = self.masks[0]._img.size
        self.mode = self.masks[0]._img.mode
        self.num_pixels = self.size[0] * self.size[1]

        self.full_results = []
        self.thumbnail_results = []

    def AllResultImages(self):
        """
        retrieve results images for the batch
        Will return empty list if makeimages
        is set to False
        """

        for image in self.full_results:
            yield image

    def AllResultThumbnails(self):
        """
        retreive results thumbnails for the batch.
        Will return empty list if makethumbnails
        is set to False
        """

        for image in self.thumbnail_results:
            yield image

    def image_objs_by_names(self, names):
        """
        Given a list of Mask or Marker names,
        return the appropriate object. Order not guaranteed.
        """

        for image_obj in (self.masks + self.markers):
            if image_obj.name in names:
                yield image_obj

    def parse_operation(self, operation):
        """
        Parses an operation into its resulting masks and marker.
        Assumes just one marker.

        :param str operation: One of the white list operations of the
            form: "mask under all, mask, components"

        :return tuple(Marker, [Masks]):
        """

        split_under = operation.split('under')

        delimeted_markers = split_under[0]
        marker_names = delimeted_markers.split(',')

        delimeted_masks = split_under[1]
        mask_names = delimeted_masks.split(',')

        logger.debug("Found marker_names: {0}".format(marker_names))
        logger.debug("Found mask_names: {0}".format(mask_names))

        # Assumption: we are under the constraint of just one marker per
        # operation
        marker = list(self.image_objs_by_names(marker_names))[0]
        masks = list(self.image_objs_by_names(mask_names))

        return marker, masks

    def cumulative_mask_indices(self, mask_components):
        '''
        Produces a np array with mask indices, corresponding
        to the intersection of all mask components.
        '''

        # initialize the eventual combined mask to all 0s
        mask_indices = np.arange(0, self.num_pixels)
        for mask in mask_components:
            # like a cumsum of intersections...
            mask_indices = GetIntersection(
                mask_indices, mask.masked_indices.flatten())

        return mask_indices

    def add_to_results_lists(self, mask_indices, marker, name):
        """
        Add output masks and markers to result lists according to
        makeimages and makethumbnails flags in BatchImage instance.
        """

        # add images to image results
        if self.makeimages:
            self.full_results.append(
                (self.MakeMaskImage(mask_indices), name + " Mask"))
            self.full_results.append(
                (self.MakeOverlayImage(mask_indices, marker), name + " Marker"))

        # add thumbnails to image results
        if self.makethumbnails:
            self.thumbnail_results.append(
                (self.MakeMaskThumbnails(mask_indices), name + " Mask"))
            self.thumbnail_results.append(
                (self.MakeOverlayThumbnails(mask_indices, marker), name + " Marker"))

    def perform_ops(self, imageout=False, thumbnails=False):
        """
        Generator to perform operations on data and images.
        Attempts to perform all calculations defined in
        BatchImage.calculations.
        """

        for operation in self.white_list:
            logger.debug(
                "Attempting to perform operation named: {0}".format(operation))

            marker, masks = self.parse_operation(operation)
            mask_indices = self.cumulative_mask_indices(masks)

            values = values_from_overlay(mask_indices, marker)
            indices = indices_from_overlay(mask_indices, marker)

            assert(values.size == indices.size)

            self.add_to_results_lists(mask_indices, marker, operation)

            yield self.calculations(
                values, indices, mask_indices, operation)

    def calculations(self, result_values, result_indices, mask_indices, name):
        """
        returns an OrderedDict of keys and values where
        key is operation name and value is the result of
        the named operation.

        You can change which calculations are performed by
        editing this function. Please don't delete existing
        calculations, just comment them out (you might want
        them later!). Each entry should be of the form:

        result_dict['calculation name'] = result_value

        E.g. calculations['<overlay name>' + 'mean'] = mean_value
        """

        # results go here under name, value pairs in dict
        result_dict = OrderedDict()
        exception_msg = "{op_name} failed for {result_name}"

        # Add or remove(comment out) calculations here
        try:
            result_dict[name + ' mean'] = result_values.mean()
        except:
            logger.exception(exception_msg.format('mean', name))
        try:
            result_dict[name + ' median'] = np.median(result_values)
        except:
            logger.exception(exception_msg.format('median', name))
        try:
            result_dict[name + ' st.dev'] = result_values.std()
        except:
            logger.exception(exception_msg.format('st.dev', name))
        try:
            result_dict[name + ' pcnt. coverage r.t. image'] = repr(
                (float(result_values.size) / self.num_pixels) * 100)
        except:
            logger.exception(exception_msg.format('pcnt. coverage r.t. image', name))
        try:
            result_dict[name + ' pcnt. coverage r.t. mask'] = repr(
                (float(result_values.size) / float(mask_indices.size)) * 100)
        except:
            logger.exception(exception_msg.format('pcnt. coverage r.t. mask', name))
        try:
            result_dict[name + ' total intensity'] = result_values.cumsum()[-1]
        except:
            logger.exception(exception_msg.format('total intensity', name))
        try:
            result_dict[
                name + 'integrated intensity r.t. mask'] = float(result_values.cumsum()[-1]) / mask_indices.size
        except:
            logger.exception(exception_msg.format('integrated intensity r.t. mask', name))

        return result_dict

    def MakeMaskImage(self, mask_indices):
        """
        Given a list of mask indices, returns an image representation
        of the mask with background black(0) and white masks area(255)
        """

        mask = np.zeros((self.num_pixels,))

        for index in mask_indices:
            mask[index] = 255

        image = Image.new(self.markers[0]._img.mode, self.markers[0].size)

        image.putdata(mask.tolist())

        return image

    def MakeOverlayImage(self, mask_indices, marker):
        """
        Given mask indices and a marker, returns an image
        with a black background and the underlying marker
        pixels (only the marker pixels under the mask)
        """

        # initialize an empty array of zeros(black pixels)
        ret_image = np.zeros((self.num_pixels,))

        indices = GetIntersection(mask_indices, marker.masked_indices)

        pixel_list = np.asarray(marker.pixel_list)

        for index in indices:
            ret_image[index] = pixel_list[index]

        # a new empty image of the same type and size as our mask/markers
        image = Image.new(self.markers[0]._img.mode, self.markers[0].size)

        image.putdata(ret_image.tolist())

        return image

    def MakeMaskThumbnails(self, mask_indices):
        """
        delegates to MakeMaskImage and creates thumbnail
        """

        img = self.MakeMaskImage(mask_indices)

        img.thumbnail((128, 128))
        return img

    def MakeOverlayThumbnails(self, mask_indices, marker):
        """
        delegates to MakeOverlayImage and creates thumbnail
        """

        img = self.MakeOverlayImage(mask_indices, marker)

        img.thumbnail((128, 128))

        return img


def IndicesByThreshold(pixel_list, threshold, op):
    """
    Returns a numpy array of indices such that each
    item in the array is an index of the input list
    as identified by the op parameter.

    E.g. if you want all indices where the pixel value
    is greater than the threshold, pass in 'operator.gt'
    """

    pixel_arr = np.asarray(pixel_list)
    indices = np.argwhere(op(pixel_arr, threshold))

    return indices


def values_from_overlay(mask_indices, marker):
    """
    Reveals the values of a marker underneath a mask.
    Takes in a numpy array of valid indices and returns
    a numpy array of marker values at those indices.
    """

    # First we need just those indices that satisfy both thresholds
    indices = GetIntersection(mask_indices, marker.masked_indices)
    # Also grab an array of all marker pixel values
    marker_pixels = np.asarray(marker.pixel_list)

    # give me the values of marker_pixels under our indices
    values = marker_pixels[indices.flatten()]

    return values


def indices_from_overlay(mask_indices, marker):
    """
    returns indices from an overlay.
    Logic is simple - but semantically this makes
    more sense
    """

    return GetIntersection(mask_indices, marker.masked_indices)


def GetIntersection(arr1, arr2):
    """
    given two arrays, returns an array with the GetArrIntersection
    of values
    """

    # TODO: check "true" flag... this could speed things up.
    return np.intersect1d(arr1, arr2)
