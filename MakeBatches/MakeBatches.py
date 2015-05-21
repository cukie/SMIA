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

# We only really need one window here...
root = Tk.Tk()
root.wm_title("MakeBatches For SMIA-CUKIE")

# A little branding to start off with
customFont = tkFont.Font(root=root,family="Helvetica", size=30)


title_label = Tk.Label(root,text="MakeBatches\nFor\nSMIA-CUKIE", font = customFont, fg='blue')

title_explain = Tk.Label(root,text="A small utility for SMIA-CUKIE\n By Gil Cukierman",fg='blue')

instructions_label = Tk.Label(root,justify=Tk.LEFT,anchor=Tk.W, text = "Choose a directory of images to make batches, then press 'MakeBatches'")

title_label.grid()
title_explain.grid()
instructions_label.grid()

root.mainloop()
