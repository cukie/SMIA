# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/28/15
# (c) All Rights Reserved

from Tkinter import Tk
from tkFileDialog import askopenfilename

# we don't want a full GUI, so keep the root window from appearing
Tk().withdraw() 

# show an "Open" dialog box and return the path to the selected file
filename = askopenfilename() 

print(filename)