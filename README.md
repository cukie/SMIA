# SMIA-CUKIE

## Simultaneous Multichannel Immunofluorescense Digital Imaging Analyzer
## By Gil Cukierman

This application was created to bulk process and analyze batches of monochromatic images providing localization(masks), intensities, and similar quantifying values(markers), including collocalizations of multichannel monochromatic imunofluorescent (or IHC, etc.) images.

It can output both image and value(excel) outputs. 

It was originally developed for use in:
>	J. Franco-Barraza et.al 2015 at the Cukierman Lab Fox Chase Cancer Center

-------------------------------------------------------------------------------------------------------------

*I am currently working on improvements to code quality, tests, documentation, and performance! Feel free to email me with any questions. gil(dot)cukierman(at)gmail* - cukie
-------------------------------------------------------------------------------------------------------------

**Please read installation instructions and relevant documentation BEFORE you begin.**

*If you wish to raise an issue with the program or extend it, please open a new issue on github or fork and open a pull request.*

**Installation:**

To install this application, the following items must be installed:

python 2.7
	Download Link:
	https://www.python.org/downloads/windows/

	A good reference to get things working:
	https://docs.python.org/2/faq/windows.html

Microsoft Visual Basic C++ for Python (Windows Only)
	https://www.microsoft.com/en-us/download/details.aspx?id=44266

Once the above to items have been installed, open a terminal(mac) or command prompt(windows) and run the following:
>	$ pip install Pillow
>	$ pip install numpy (must have C++ compiler on Windows above)



You can then download the source code in two ways:
* from this github site (find the 'download zip' button on the side)
* using git clone (https and ssh options both given on the side bar)



**RUNNING FROM THE GRAPHICAL INTERFACE:**

To run SMIA-CUKIE using the graphical interface, just double click on SMIA-CUKIE.py

To run MakeBatches utility using the graphical interface, just double click on MakeBatches.py

<br>
*An example configuration file and images to test on have been provided in production_testers*
<br>
<br>
*If you don't plan on running this application from the command line, you may stop here*
<br>
<br>
<br>
<br>
 



**RUNNING FROM THE COMMAND LINE:**
The application functionality can also be accessed via the command line. In order to do this,
please follow the instructions below carefully. This functionality requires you to create a 
configuration file in a text editor and can be a little more technical. 

*Use of the graphical interface is recommended.*

**Image Format and Directory Structure:**

The "base directory" will be a folder that holds all other folders. A typical file structure for analyzation MUST be of this form:

	Base_Directory
		-> Batch1_Directory
			-> Image1
			-> Image2
			-> Image3
			-> Image4
			-> Image5
			... no limit on picture numbers

		-> Batch2_Directory
                        -> Image1
                        -> Image2
                        -> Image3
                        -> Image4
                        -> Image5
                        ... all directories must contain same number of images

		-> More_Batches!!!!!
                        -> Image1
                        -> Image2
                        -> Image3
                        -> Image4
                        -> Image5
                        ... name your images whatever you want but stay consistent between batches. 


**Configuration:**

For every run of the application, you must first create a configuration file. A default ConfigMe file can be created by running the following in terminal or command prompt:
	
> 	$ python make_config.py

A default configuration file skin named ConfigMe will be created.

Copy ConfigMe and rename it to something meaningful, and proceed to 
fill in the fields of the JSON formatted file. Each field has a key
and a value formatted as - key:value.

DO NOT CHANGE THE KEYS - ONLY THE VALUES. DO NOT LEAVE ANY DEFAULT VALUE INFORMATION IN THE CONFIGURATION FILE.

Replace each descriptor value with the information it asks for. For clarification purposes, all the configuration options are described below:
	
	base_directory: 
		A string representing the absolute path of the top level directory containing all the batches of images. NOTE 			in Windows you will need to use double backslashes.
		E.g. Windows - "C:\\path\\to\\dir\\here"
			 Mac - "/path/to/dir/here"

	marker_names:
		A list of all markers in the following format:
			[file prefix, desired name, threshold]

			file prefix - a unique identifier for the name of this specific image frame. 

			desired name - the name you would like to use to identify the file. This is the name that will 					represent the marker in your results. 

			threshold - a threshold value for your marker where a valid pixel is defined as having a value greater 			than or equal to the threshold. 

	mask_names:
		A list of mask names defined the same way as marker names

	num_markers: 
		integer value of number of markers 

	num_masks:
		integer value of number of masks

	num_pictures:
		integer value of total number of images per batch

	overlay_white_list:
		a list of strings corresponding to the operations you would like the application to perform. They must all be 			of the form "singlemarker under however, many, masks"

		In order to denote the inverse of a mask or marker, simply prepend the word "NOT" to the front of the name. 			E.g. if we have a marker called nuclei, then its inverse would be NOTnuclei. 

	output_to:
		A string representing the absolute path of where you wish to output all results (excel file, copy of 				configuration file used, thumbnails, etc.)


**RUNNING INSTRUCTIONS:**

Before you run the program please make sure that all fields in the configuration file have been filled out appropriately. 

To run the program, open a terminal(mac) or command prompt(windows), and type the following command:
	
>	$ python images.py [/path/to/config/file/omit/brackets]

If the program runs successfully (can take several minutes if there are many images and/or operation to analyze) you will see a message telling you that 'you have successfully proccessed:' your images, and where you can find your results. 

**QUESTIONS/COMMENTS:**

For general inquiries please contact **Dr. Edna Cukierman**

**If you wish to raise an issue with the program or extend it, please open a new issue on github or fork and open a pull request.**

