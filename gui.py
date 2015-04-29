# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/28/15
# (c) All Rights Reserved

# A small module to work with getting information from GUI

from Tkinter import Tk
from tkFileDialog import askdirectory

# Opens a file open dialog for the user and asks for the parent directory
def getParentFile():
	# we don't want a full GUI, so keep the root window from appearing
	Tk().withdraw() 

	# show an "Open" dialog box and return the path to the selected file
	filename = askdirectory() 

	return filename