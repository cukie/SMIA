# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 5/21/15
# (c) All Rights Reserved

"""
A simple GUI that allows a user to specify a location of 
a raw output dump of images and group them into "batches"
in another directory.

Parsing used in make_batches is specific to the Cukierman lab
use cases, but could be used as an example of the proper 
format to feed into the SMIA-CUKIE application (and how
to automate this process).
"""

import Tkinter as Tk
import tkFileDialog
import tkFont
import tkMessageBox
import make_batches

def getdirectory():
	"""
	Show a file dialog to ask for a directory
	update the text box with the new directory 
	path.
	"""

	directory = tkFileDialog.askdirectory()
	directory_entry.delete(0,Tk.END)
	directory_entry.insert(0,directory)

def RunMakeBatches():
	"""
	Runs make_batches.main(directory), where directory
	is the text that appears in the Entry box.
	"""
	directory = directory_entry.get()
	root.destroy()

	make_batches.main(directory)
	# try:
	# 	MakeBatches.main(directory)
	# 	Tk.Tk().withdraw()
	# 	tkMessageBox.showinfo("Success! \nBatches Made!")
	# except:
	# 	# Give error window
	# 	Tk.Tk().withdraw()
	# 	tkMessageBox.showerror("Error! \nPlease check terminal output.")

# We only really need one window here...
root = Tk.Tk()
root.wm_title("MakeBatches For SMIA-CUKIE")

# A little branding to start off with
customFont = tkFont.Font(root=root,family="Helvetica", size=30)
title_label = Tk.Label(root,text="MakeBatches\nFor\nSMIA-CUKIE", font = customFont, fg='blue')
title_explain = Tk.Label(root,text="A small utility for SMIA-CUKIE\n By Gil Cukierman",fg='blue')

# Our instructions
instructions_label = Tk.Label(root,justify=Tk.LEFT,anchor=Tk.W, text = "\n\nChoose a directory of images to make batches, then press 'MakeBatches'")

# Our Entry box and our browse button
directory_entry = Tk.Entry(root, width = 60)
directory_entry.insert(0,"Directory of 8-bit images")
browse_button = Tk.Button(root, text="Browse",command=getdirectory)

run_button = Tk.Button(root, text="MakeBatches",command=RunMakeBatches)

# Pack it all in to our window
title_label.grid()
title_explain.grid()
instructions_label.grid()
directory_entry.grid(row=4,column=0)
browse_button.grid(row=4,column=1)
run_button.grid()

root.mainloop()
