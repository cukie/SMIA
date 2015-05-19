# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/28/15
# (c) All Rights Reserved


import Tkinter as Tk
import tkFileDialog
import os
from sets import Set
import itertools

def isuseless(name_list):
    for name in name_list:
        if "NOT" + name in name_list:
            return True

    return False

def createdict():
    global basedir, output_dir,nummasks,nummarkers,mask_list,marker_list,output_images,output_thumbnails,white_list

    config = {}
    
    config['base_directory'] = basedir
    config['num_pictures'] = nummasks+nummarkers
    config['num_masks'] = nummasks
    config['mask_names'] = mask_list
    config['num_markers'] = nummarkers
    config['marker_names'] = marker_list
    config['overlay_white_list'] = white_list
    config['output_images'] = output_images
    config['output_thumbnails'] = output_thumbnails
    config['output_to'] = output_dir

    return config    

def createalloverlaynames():
    global mask_list
    mask_names_ = [x[1] for x in mask_list] #grab all mask names
    marker_names_ = [x[1] for x in marker_list] # grab all marker names

    mask_names = []
    marker_names = []
    for name in mask_names_:
        mask_names.append(name)
        mask_names.append("NOT"+name)

    for name in marker_names_:
        marker_names.append(name)
        marker_names.append("NOT"+name)

    all_together = mask_names + marker_names

    all_together = Set(all_together)

    combinations = []

    marker_combos = []
    for i in xrange(1,len(all_together)+1):
            for marker_combination in itertools.combinations(all_together,i):
                if not isuseless(marker_combination):
                    marker_combos.append(marker_combination)

    # for every mask, generate all combinations
    for combo in itertools.product(marker_names,marker_combos):
        marker = combo[0]
        mask = combo[1]

        overlay = marker + " under " + ", ".join(mask)
        combinations.append(overlay)
        # generate all combinations
        
    return combinations


def GetPicList(basedir):
    """
    base_dir
        -> batch1
            -> we 
            -> want
            -> these
            -> images
        -> batch2
    """

    pic_list = os.listdir(os.path.join(basedir,(os.listdir(basedir)[2])))

    return pic_list

def firstthings():
    global basedir,nummasks,nummarkers, output_images, output_thumbnails, output_dir, imaging_stack_loc
    basedir = basedir_entry.get()
    nummasks = int(nummasks_entry.get())
    nummarkers = int(nummarkers_entry.get())
    output_images = True if output_images_var.get() else False
    output_thumbnails = True if output_thumbnails_var.get() else False
    imaging_stack_loc = proloc_entry.get()
    root.destroy()

def maskthings():

    global mask_list
    for prefix,name,threshold in mask_objects:
        prefix = prefix.get()
        name = name.get()
        threshold = threshold.get()

        mask_list.append((prefix,name,threshold))

    masks.destroy()

def markerthings():

    global marker_list

    for prefix,name,threshold in marker_objects:
        prefix = prefix.get()
        name = name.get()
        thresh = threshold.get()

        marker_list.append((prefix,name,thresh))

    markers.destroy()

def addtowhitelist():
    # On Enter, grab the option, and add it to the label list
    global white_list
    # create a label, and add it to the grid
    op = overlay_var.get()
    new_label = Tk.Label(white,fg='blue',text=op)
    new_label.grid(columnspan=2)
    white_list.append(op)

def whitelistcontinue():
    # we have our white list continue
    white.destroy()

def setbase():
    global basedir_entry

    directory = tkFileDialog.askdirectory()

    basedir_entry.delete(0,Tk.END)
    basedir_entry.insert(0, directory)

def setresults():
    global output_dir

    directory = tkFileDialog.askdirectory()

    outdir_entry.delete(0,Tk.END)
    outdir_entry.insert(0, directory)

def setlocation():
    global imaging_stack_loc

    directory = tkFileDialog.askdirectory()

    basedir_entry.delete(0,Tk.END)
    basedir_entry.insert(0, directory)



if __name__ == '__main__':

    ################ First Window ############################

    root = Tk.Tk()
    root.wm_title("Initial Options")


    ### OUR EVENTUAL CONFIGURATION VARIABLES ###
    basedir = 'default'
    output_dir = 'default'
    nummasks = 'default'
    nummarkers = 'default'
    mask_list = []
    marker_list = []
    white_list = []
    output_images = False
    output_thumbnails = False 

    imaging_stack_loc = os.path.join(os.path.expanduser('~'),"imaging_stack")

    program_loc_label = Tk.Label(root,anchor=Tk.CENTER,fg='red',text="MAKE SURE THIS PATH CORRESPONDS TO THE LOCATION OF YOUR 'imaging_stack' directory")
    program_loc_label.grid(columnspan=2)

    proloc_entry = Tk.Entry(root, width=80)
    proloc_entry.insert(0, imaging_stack_loc)
    browse3 = Tk.Button(root, text="Browse", command = setlocation)

    basedir_entry = Tk.Entry(root, width=80)
    basedir_entry.insert(0, "Base Directory")
    browse1 = Tk.Button(root, text="Browse", command = setbase)

    outdir_entry = Tk.Entry(root, width=80)
    outdir_entry.insert(0, "Results Directory")
    browse2 = Tk.Button(root, text="Browse", command = setresults)

    nummasks_entry = Tk.Entry(root)
    nummasks_entry.insert(0, "How many masks?")

    nummarkers_entry = Tk.Entry(root)
    nummarkers_entry.insert(0, "How many markers?")

    output_images_var = Tk.IntVar()
    output_images_button = Tk.Checkbutton(root, text="Output Full-Sized Images", variable=output_images_var)

    output_thumbnails_var = Tk.IntVar()
    output_thumbnails_button = Tk.Checkbutton(root, text="Output Full-Sized Images", variable=output_thumbnails_var)

    pressme = Tk.Button(root, text="Continue", command = firstthings)
    proloc_entry.grid(row=1,column=0)
    browse3.grid(row=1,column=1)
    basedir_entry.grid(row=2,column=0)
    browse1.grid(row=2,column=1)
    outdir_entry.grid(row=3,column=0)
    browse2.grid(row=3,column=1)
    nummasks_entry.grid()
    nummarkers_entry.grid()
    output_images_button.grid()
    output_thumbnails_button.grid()
    pressme.grid()
    root.mainloop()


    ################### Second Window ###############################
    masks = Tk.Tk()
    masks.wm_title("Mask Options")
    mask_objects = []
    dir_list = GetPicList(basedir)

    mask_label = Tk.Label(masks, text="Mask Options")
    mask_label.grid()

    for i in range(nummasks):
        # prefix = Tk.Entry(masks)
        # prefix.insert(0, "mask prefix")


        prefix_var = Tk.StringVar(masks)
        prefix_var.set("Choose Mask Prefix") # initial value
        prefix = apply(Tk.OptionMenu, (masks,prefix_var) + tuple(dir_list))
       
        name = Tk.Entry(masks)
        name.insert(0, "mask name")

        threshold = Tk.Scale(masks, from_=0, to=255, orient=Tk.HORIZONTAL, label="threshold", length=255)

        prefix.grid(row=i, column=0)
        name.grid(row=i, column=1)
        threshold.grid(row=i, column=2)

        mask_objects.append((prefix_var,name,threshold))

    pressme = Tk.Button(masks, text="Continue", command = maskthings)
    pressme.grid()
    masks.mainloop()
    print "done masks..."



    ################ Third Window ###############################################

    markers = Tk.Tk()
    markers.wm_title("Marker Options")
    marker_objects = []
    dir_list = GetPicList(basedir)

    marker_label = Tk.Label(markers, text="Marker Options")
    marker_label.grid()

    for i in range(nummarkers):
        # prefix = Tk.Entry(masks)
        # prefix.insert(0, "mask prefix")


        prefix_var = Tk.StringVar(markers)
        prefix_var.set("Choose Marker Prefix") # initial value
        prefix = apply(Tk.OptionMenu, (markers,prefix_var) + tuple(dir_list))
       
        name = Tk.Entry(markers)
        name.insert(0, "Marker name")
        
        threshold = Tk.Entry(markers)
        threshold.insert(0, "Marker threshold")

        threshold = Tk.Scale(markers, from_=0, to=255, orient=Tk.HORIZONTAL, label="threshold", length=255)

        prefix.grid(row=i, column=0)
        name.grid(row=i, column=1)
        threshold.grid(row=i, column=2)

        marker_objects.append((prefix_var,name,threshold))

    pressme = Tk.Button(markers, text="Continue", command = markerthings)
    pressme.grid()
    masks.mainloop()
    print "done markers..."


    ############## White List ######################
    white = Tk.Tk()
    white.wm_title("Choose Overlays")


    all_options = createalloverlaynames()

    overlay_var = Tk.StringVar(white)
    overlay_var.set("Choose Which Overlays to Perform") # initial value
    overlay_options = apply(Tk.OptionMenu, (white,overlay_var) + tuple(all_options))

    enter_button = Tk.Button(white, text="Enter", command = addtowhitelist)

    pressme = Tk.Button(white, text="Continue", command = whitelistcontinue)


    overlay_options.grid(row=0,column=0)
    enter_button.grid(row=0,column=1)
    pressme.grid()


    white.mainloop()




    config_dict = createdict()
    print config_dict
    # config_path = makeconfigfile(config_dict)


 






