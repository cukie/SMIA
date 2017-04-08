#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukie
# @Date:   2015-09-02 17:56:53
# @Last Modified by:   cukie
# @Last Modified time: 2016-02-09 21:30:33

import unittest
import mock
from smiaCukie import batch_image, batch_runner


class TestBatchRunner(unittest.TestCase):
    def setUp(self):

        # We set up a BatchRunner object as a fixture here... We will
        # test the creation of the object in it's own function, but
        # It's useful for all the other tests to have access to it here.
        self.batchRunnerFixture = batch_runner.BatchRunner(
            'test/base/dir',  # base_dir
            4,  # num_layers
            2,  # num_masks
            2,  # num_markers
            [["first", "firstMask", 10], ["second", "secondMask", 20]],  # mask_names
            [["third", "firstMaarker", 30], ["fourth", "fourthMarker", 40]],  # marker_names
            {'third under first': 'third under first'},  # white_list
            False,  # output_images
            False,  # output_thumbnails
            "test/out/path"  # output_path
        )

    def testBatchRunnerConstructor(self):
        '''maybe silly... But for completeness, check that our constructor sets its properties correctly. Enforce that our constructor does nothing.'''
        self.assertEqual(self.batchRunnerFixture.base_dir, 'test/base/dir')
        self.assertEqual(self.batchRunnerFixture.num_layers, 4)
        self.assertEqual(self.batchRunnerFixture.num_masks, 2)
        self.assertEqual(self.batchRunnerFixture.num_markers, 2)
        self.assertEqual(self.batchRunnerFixture.mask_names, [["first", "firstMask", 10], ["second", "secondMask", 20]])
        self.assertEqual(self.batchRunnerFixture.marker_names,
                         [["third", "firstMaarker", 30], ["fourth", "fourthMarker", 40]])
        self.assertEqual(self.batchRunnerFixture.white_list, {'third under first': 'third under first'})
        self.assertEqual(self.batchRunnerFixture.output_images, False)
        self.assertEqual(self.batchRunnerFixture.output_thumbnails, False)
        self.assertEqual(self.batchRunnerFixture.output_path, "test/out/path")

    def testMaskOrMarkerMaskPath(self):
        '''test that we can appropriately parse our mask_names and marker_names list and determine a mask path'''

        expectedResult = "mask"

        # Call _maskOrMarker with a path that will trigger a return value of mask
        actualResult = self.batchRunnerFixture._maskOrMarker('first/things/first/im/the/realest')

        self.assertEqual(actualResult, expectedResult, 'Can we correctly find masks in _maskOrMarker()?')

    def testMaskOrMarkerMarkerPath(self):
        '''test that we can appropriately parse our mask_names and marker_names list and determine a marker path'''

        expectedResult = "marker"

        # Call _maskOrMarker with a path that will trigger a return value of marker
        actualResult = self.batchRunnerFixture._maskOrMarker('may/the/fourth/be/with/you')

        self.assertEqual(actualResult, expectedResult, 'Can we correctly find markers in _maskOrMarker()?')

    def testMaskOrMarkerPhonyPath(self):
        '''test that when given a phony path, we raise a ValueError with the appropriate message'''

        phonyPath = 'haters/gonna/hate/hate/hate/hate/hate'
        expectedBaseMessage = 'given marker or mask prefix not found while traversing directory for image: '
        with self.assertRaises(ValueError) as assertion:
            self.batchRunnerFixture._maskOrMarker(phonyPath)

        self.assertEqual(assertion.exception.message, expectedBaseMessage + phonyPath)

    @mock.patch('smiaCukie.batch_runner.BatchRunner._getImage')
    def testCreateSinglePicObjectTrueNegativeFlag(self, get_image):
        """"Test that given a pic_path, we can create the appropriate
         pic obj aka Mask or Marker. This test will 
         have withNegative=True
         """

        # This should trigger a couple of Mask objects.
        pic_path = 'the/first/cut/is/the/deepest/first'
        actual_result = self.batchRunnerFixture._createSinglePicObj(
            pic_path,
            withNegative=True
        )

        # first make sure we got the right number of objects
        self.assertEqual(len(actual_result), 2)

        # then make sure that they are Mask objects
        for result in actual_result:
            self.assertIsInstance(result, batch_image.Mask)

        # This should trigger a couple of Marker objects.
        pic_path = 'third/eye/blind/third'
        actual_result = self.batchRunnerFixture._createSinglePicObj(
            pic_path, withNegative=True
        )

        self.assertEqual(len(actual_result), 2)
        print actual_result
        for result in actual_result:
            print result
            self.assertIsInstance(result, batch_image.Marker)

    @mock.patch('smiaCukie.batch_runner.BatchRunner._getImage')
    def testCreateSinglePicObjectFalseNegativeFlag(self, imageGetter):
        """Test that given a pic_path, we can create the appropriate 
        Mask or Marker. This test will have withNegative=False
        """

        # See that we can do this for Masks
        pic_path = 'second/to/none/third'
        actual_result = self.batchRunnerFixture._createSinglePicObj(
            pic_path,
            withNegative=False
        )

        self.assertEqual(len(actual_result), 1)
        self.assertIsInstance(actual_result[0], batch_image.Mask)

        # Check for Markers
        pic_path = 'fourth/and/inches/fourth'
        actual_result = self.batchRunnerFixture._createSinglePicObj(
            pic_path,
            withNegative=False
        )
        self.assertEqual(len(actual_result), 1)
        self.assertIsInstance(actual_result[0], batch_image.Marker)


if __name__ == '__main__':
    unittest.main()
