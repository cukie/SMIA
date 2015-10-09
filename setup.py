#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cukierma
# @Date:   2015-09-01 04:55:05
# @Last Modified by:   cukierma
# @Last Modified time: 2015-09-02 06:56:37

'''Our install specifications for SMIA_CUKIE'''

from setuptools import setup, find_packages

setup(
	name = 'SMIA',
	version = '0.01',
	description = 'Simultaneous Multi-Channel Immunofluorescence Analysis',
	author = 'Gil Cukierman',
	author_email = 'gil.cukierman@gmail.com',
	packages = find_packages(),
	requires = ['Pillow', 'numpy', 'mock'],
	)