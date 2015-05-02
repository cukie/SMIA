# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/2/15
# (c) All Rights Reserved

import json

"""Creates a json skin for a configuration file that the user can fill out"""

if __name__ == "__main__":

	config = {}
	
	config['base_directory'] = "full path"
	config['num_pictures'] = "number of layers"
	config['num_masks'] = "number of masks"
	config['mask_names'] = [('file_prefix','name'),('file_prefix2','name2')]
	config['num_markers'] = "number of markers"
	config['marker_names'] = [('file_prefix','name'),('file_prefix2','name2')]


	# output options
	config['output_to'] = "full output path"



	json = json.dumps(config, indent=4, sort_keys=True)

	with open('ConfigMe', 'w+') as config_file:
		config_file.write(json)