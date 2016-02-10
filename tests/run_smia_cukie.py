#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukie
# @Date:   2015-08-30 12:04:40
# @Last Modified by:   cukie
# @Last Modified time: 2016-02-09 21:28:56

import unittest
import mock
from ..smiaCukie import run_smia_cukie

class TestRunSmiaCukie(unittest.TestCase):
	'''Testing the functionality of SMIA-CUKIE.SMIA-CUKIE.run_smia_cukie.py'''
	def setUp(self):
		# A config dict fixture
		self.configuration_dict = {
			'base_dir':'base',
			'num_layers':'num',
			'num_masks':'mask',
			'num_markers':'marker',
			'mask_names':'names',
			'marker_names':'nombres',
			'output_path':'output',
			'overlay_white_list':'a',
			'output_images':'images',
			'output_thumbnails':'thumbnails',
		} 

	@mock.patch('SMIA.smiaCukie.run_smia_cukie.batch_runner.BatchRunner')
	def testBatchRunnerFromConfigDict(self, batchrunner):
		'''Test that we are grabbing parameters from the dict and creating a BatchRunner Object'''
		run_smia_cukie.batchRunnerFromConfigDict(self.configuration_dict)
		batchrunner.assert_called_with(self.configuration_dict['base_dir'],
										self.configuration_dict['num_layers'],
										self.configuration_dict['num_masks'],
										self.configuration_dict['num_markers'],
										self.configuration_dict['mask_names'],
										self.configuration_dict['marker_names'],
										{self.configuration_dict['overlay_white_list']:self.configuration_dict['overlay_white_list']},
										self.configuration_dict['output_images'],
										self.configuration_dict['output_thumbnails'],
										self.configuration_dict['output_path'],
		)
		

if __name__ == '__main__':
    unittest.main()
