#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukie
# @Date:   2015-08-30 12:04:40
# @Last Modified by:   cukie
# @Last Modified time: 2015-09-01 06:16:33

import unittest
import mock
import SMIA_CUKIE.smiaCukie.run_smia_cukie

class TestRunSmiaCukie(unittest.TestCase):
	'''Testing the functionality of SMIA-CUKIE.SMIA-CUKIE.run_smia_cukie.py'''
	def setUp(self):
		# A sentinel config dict 
		self.configuration_dict = {
			'base_dir':'',
			'num_layers':'',
			'num_masks':'',
			'num_markers':'',
			'mask_names':'',
			'marker_names':'',
			'output_path':'',
			'overlay_white_list':'',
			'output_images':'',
			'output_thumbnails':'',
		} 

	@mock.patch('SMIA_CUKIE.smiaCukie.run_smia_cukie.batch_runner.BatchRunner')
	def testBatchRunnerFromConfigDict(self, batchrunner):
		'''Test that we are grabbing parameters from the dict and creating a BatchRunner Object'''
		print batchrunner

if __name__ == '__main__':
    unittest.main()
