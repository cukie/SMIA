# SMIA-CUKIE

#### The Simultaneous Multichannel Immunofluorescence Digital Imaging Analyzerby Gil Cukierman
---

This application was created to bulk process and analyze batches of monochromatic images providing localization (masks),
intensities, and similar quantifying values (markers), including co-localizations of multichannel monochromatic
immunofluorescent (or IHC, etc.) images. It creates both image and value (excel) outputs.  

It was originally developed for use in:
>	J. Franco-Barraza et.al 2017. *eLife* http://dx.doi.org/10.7554/eLife.20600 
>       Cukierman Lab
>	Fox Chase Cancer Center, Philadelphia, PA 19111.


### Installation
You can install a Windows executable for the latest version of SMIA at https://github.com/cukie/SMIA/releases/tag/2.0.0
If you want to build from source, or are on a platform other than windows,
download or clone the source code and run...
```python
python smia/setup.py
python smia/smia_ui.py
```
Note that to build from source, you'll need Python 2.7 and a C++ compiler.
The C++ compiler for Windows can be found at https://www.microsoft.com/en-us/download/details.aspx?id=44266


### Running From the Graphical Interface
To run the SMIA user interface, run the executable or from source:
```python
python smia.run_smia_cukie config_file.txt
```
A script and ui to aid in making `batches` can also be downloaded and run
as a Windows executable. This was developed specifically for the Cukierman
lab, and will probably be of no use to others. To run from source...
```python
python batch_maker_ui.py
```

### Tests and sample data
If downloading the source, unit tests can be found in the `tests` package.
Some sample batches and sample images can be found in `tests/test_fixtures/test_images`
You can run them by editing `tests/test_fixtures/test_images_config.config` to
point to the `base_dir` and `output_to` the correct paths on your system. 
From the command line...
```python
python smia/run_smia_cukie tests/test_fixtures/test_images_config.config
```

### Image Format and Directory Structure:

The base directory for images will be a folder that holds all other folders. 
Each folder is a "batch" and a typical file structure for analysis must
be in the following format:

	Base_Directory
		-> Batch1_Directory
			-> Image1
			-> Image2
			-> Image3
			-> Image4
			-> Image5

		-> Batch2_Directory
            -> Image1
            -> Image2
            -> Image3
            -> Image4
            -> Image5

		-> More_Batches as needed...
            -> etc...

### Naming images, masks, and markers
 1. mask and marker names unique
 2. mask and marker names must not be a subset of each other
 3. each mask or marker name must correspond uniquely to an image name 
 in each batch
 4. Note that the names of images will be identified by the image file name
 and only characters after the final `]` character will be included. `]` is
 not a necessary component of the image name. This is to keep compatibility
 with the format of the imaging mechanism first used for the original study.

### Configuration parameters
For every run of the application, you must first create a configuration file.
Configuration files are just plain JSON.
A sample config file can be seen in `sample_config.txt` 
		
	base_directory: 
		A string representing the absolute path of the top level 
		directory containing all the batches of images.
		NOTE in Windows you will need to use double backslashes as escapes.
		E.g. Windows - "C:\\path\\to\\dir\\here"
		*nix - "/path/to/dir/here"

	marker_names:
	    A list of all markers in the following format: [file prefix, desired name, threshold]
	    file prefix - a unique identifier for the name of this specific image frame. See restriction on names above.
	    desired name - the name you would like to use to identify the file. This is the name that will represent the marker in your results. 
        threshold - a threshold value for your marker where a valid pixel is defined as having a value greater than or equal to the threshold. 

	mask_names:
		A list of mask names defined the same way as marker names

	num_markers: 
		integer value of number of markers (this will be removed soon)

	num_masks:
		integer value of number of masks (this will be removed soon)

	num_pictures:
		integer value of total number of images per batch (this will be removed soon)

	overlay_white_list:
		a list of strings corresponding to the operations you would like the application to perform. They must all be of the form "singlemarker under however, many, masks" In order to denote the inverse of a mask or marker, simply prepend the word "NOT" to the front of the name. 
		E.g. if we have a marker called nuclei, then its inverse would be NOTnuclei. (The name of this parameter is weird and will change in the future)

	output_to:
		A string representing the absolute path of where you wish to output all results (excel file, copy of configuration file used, thumbnails, etc.)

### Issues and Feedback
For general inquiries about the papaer please contact *Dr. Edna Cukierman.*
https://www.foxchase.org/edna-cukierman
Email: EdnaCukierman@gmail.com

If you find issues with the software, please file a github issue.
