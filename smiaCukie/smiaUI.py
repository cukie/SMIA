# Author: Gil Cukierman
# gil.cukierman (at) gmail.com
# Creation Date: 4/28/15
# (c) All Rights Reserved


import Tkinter as Tk
import tkFileDialog
import tkMessageBox
import os
from sets import Set
import itertools
import json
import run_smia_cukie
import sys
import tkFont


def runanalysis(config_path):
    try:
        # TODO: add logging and other command line flags here.
        namespace = run_smia_cukie.get_args_namespace([config_path])
        run_smia_cukie.run_smia_cukie(namespace)
        Tk.Tk().withdraw()  # get rid of top level window
        tkMessageBox.showinfo("Success!,", "Success!!!\n")
    except:
        Tk.Tk().withdraw()  # get rid of top level window
        tkMessageBox.showerror("ERROR!", "An error occurred! \nSee terminal output")
        print sys.exc_info()
        sys.exit(1)


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

    filename = ''
    for name in os.listdir(basedir):
        if not name.startswith('.'):
            filename = name
            break

    if not filename:
        raise ValueError("Couldn't find any non-hidden directories in basedir")

    pic_list = os.listdir(os.path.join(basedir,filename))

    for pic in pic_list:
        pic = pic.replace('.tif','')
    return pic_list

def firstthings():
    global basedir,nummasks,nummarkers, output_images, output_thumbnails, output_dir
    basedir = basedir_entry.get()
    output_dir = outdir_entry.get()
    nummasks = int(nummasks_entry.get())
    nummarkers = int(nummarkers_entry.get())
    output_images = True if output_images_var.get() else False
    output_thumbnails = True if output_thumbnails_var.get() else False
    first_options.destroy()

def maskthings():

    global mask_list, dir_list
    for prefix,name,threshold in mask_objects:
        prefix = prefix.get()
        name = name.get()
        thresh = threshold.get()

        # make it easier later on
        for item in dir_list:
            if prefix in dir_list:
                dir_list.remove(item)

        mask_list.append((prefix,name,thresh))

    masks.destroy()

def markerthings():

    global marker_list, dir_list

    for prefix,name,threshold in marker_objects:
        prefix = prefix.get()
        name = name.get()
        thresh = threshold.get()

        # this way we remove repition errors
        for item in dir_list:
            if prefix in dir_list:
                dir_list.remove(item)

        marker_list.append((prefix,name,thresh))

    markers.destroy()

def addtowhitelistfield():
    global white_list
    op = input_entry.get()
    input_entry.delete(0,Tk.END)
    new_label = Tk.Label(white,fg='blue',text=op)
    new_label.grid(columnspan=2)
    white_list.append(op)

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
    global outdir_entry

    directory = tkFileDialog.askdirectory()

    outdir_entry.delete(0,Tk.END)
    outdir_entry.insert(0, directory)

def setlocation():
    global proloc_entry

    directory = tkFileDialog.askdirectory()

    proloc_entry.delete(0,Tk.END)
    proloc_entry.insert(0, directory)

def makeconfigfile(output_dir,output_dict):
    print output_dict
    jayson = json.dumps(output_dict, indent=4, sort_keys=True)

    config_loc = os.path.join(output_dir,"config_used.config")

    with open(config_loc, 'w+') as config_file:
        config_file.write(jayson)

    return config_loc

def setconfig():
    directory = tkFileDialog.askopenfilename()

    config_loc_entry.delete(0,Tk.END)
    config_loc_entry.insert(0, directory)

def setnewres():
    directory = tkFileDialog.askdirectory()

    result_loc.delete(0,Tk.END)
    result_loc.insert(0, directory)

def runfromconfig():
    global from_config
    # grab the new configuration file
    config_file = config_loc_entry.get()
    # update the results file
    new_result_loc = result_loc.get()

    # open the config file, load the json dict
    # change the dict and write the file back.
    to_change = {}
    with open(config_file,'rb') as f:
        to_change = json.load(f)

    to_change['output_to'] = new_result_loc

    jayson = json.dumps(to_change, indent=4, sort_keys=True)

    newloc = os.path.join(new_result_loc,'used_config.config')

    with open(newloc, 'wb') as f:
        f.write(jayson)

    from_config.destroy()

    # now pass the new file into images.py main function
    runanalysis(newloc)

    sys.exit(0)

def makenew():
    # if we get to here let's destroy the window and just move on
    from_config.destroy()

if __name__ == '__main__':


    ############### From Config ##########################
    from_config = Tk.Tk()
    from_config.wm_title("SMIA-CUKIE")

    customFont = tkFont.Font(root=from_config,family="Helvetica", size=80)


    title_label = Tk.Label(from_config,text="SMIA-CUKIE", font = customFont, fg='blue')

    title_explain = Tk.Label(from_config,text="Simultaneous Multi-Channel Immunofluorescence Analysis\n By Gil Cukierman",fg='blue')

    instructions_label = Tk.Label(justify=Tk.LEFT,anchor=Tk.W, text = "\n\nIf you already have a configuration file, proceed below and press 'Run Analysis'\nOtherwise, press 'Make New' to create a configuration file\n\n")

    config_loc_entry = Tk.Entry(from_config, width=50)
    config_loc_entry.insert(0, "Configuration File Location")
    browse = Tk.Button(from_config, text="Browse", command = setconfig)

    # browse for new results location
    result_loc = Tk.Entry(from_config, width=50)
    result_loc.insert(0, "New Result Location")
    browseres = Tk.Button(from_config, text="Browse", command = setnewres)


    run = Tk.Button(from_config, text="Run Analysis", command=runfromconfig)
    dontrun = Tk.Button(from_config, text="Make New", command=makenew)

    title_label.grid(columnspan=2)
    title_explain.grid(columnspan=2)
    instructions_label.grid()

    config_loc_entry.grid(row=4,column=0)
    browse.grid(row=4,column=1)
    result_loc.grid(row=5,column=0)
    browseres.grid(row=5,column=1)
    run.grid()
    dontrun.grid()


    from_config.mainloop()


    ################ First Options Window ############################

    first_options = Tk.Tk()
    first_options.wm_title("Initial Options")


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

    customFont = tkFont.Font(root=first_options,family="Helvetica", size=80)


    title_label = Tk.Label(first_options,text="SMIA-CUKIE", font = customFont, fg='blue')

    title_explain = Tk.Label(first_options,text="Simultaneous Multi-Channel Immunofluorescence Analysis\n By Gil Cukierman",fg='blue')

    instructions_label = Tk.Label(first_options,justify=Tk.LEFT,anchor=Tk.W, text = "\n\nFill in the options below.\nUse Caution with outputing images and thumbnails(No more than 10 batches)!!\n")

    basedir_entry = Tk.Entry(first_options, width=80)
    basedir_entry.insert(0, "Base Directory")
    browse1 = Tk.Button(first_options, text="Browse", command = setbase)

    outdir_entry = Tk.Entry(first_options, width=80)
    outdir_entry.insert(0, "Results Directory")
    browse2 = Tk.Button(first_options, text="Browse", command = setresults)

    nummasks_entry = Tk.Entry(first_options)
    nummasks_entry.insert(0, "How many masks?")

    nummarkers_entry = Tk.Entry(first_options)
    nummarkers_entry.insert(0, "How many markers?")

    output_images_var = Tk.IntVar()
    output_images_button = Tk.Checkbutton(first_options, text="Output Full-Sized Images", variable=output_images_var)

    output_thumbnails_var = Tk.IntVar()
    output_thumbnails_button = Tk.Checkbutton(first_options, text="Output Thumbnail Images", variable=output_thumbnails_var)

    pressme = Tk.Button(first_options, text="Continue", command = firstthings)
    # proloc_entry.grid(row=1,column=0)
    # browse3.grid(row=1,column=1)
    title_label.grid(columnspan=2)
    title_explain.grid(columnspan=2)
    instructions_label.grid()
    basedir_entry.grid(row=4,column=0)
    browse1.grid(row=4,column=1)
    outdir_entry.grid(row=5,column=0)
    browse2.grid(row=5,column=1)
    nummasks_entry.grid()
    nummarkers_entry.grid()
    output_images_button.grid()
    output_thumbnails_button.grid()
    pressme.grid()
    first_options.mainloop()


    ################### Mask Options Window ###############################
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
        
        common_sub = Tk.Entry(masks)
        common_sub.insert(0,"common subsequence")

        name = Tk.Entry(masks)
        name.insert(0, "mask name")

        threshold = Tk.Scale(masks, from_=0, to=255, orient=Tk.HORIZONTAL, label="threshold", length=255)

        prefix.grid(row=i, column=0)
        common_sub.grid(row=i,column=1)
        name.grid(row=i, column=2)
        threshold.grid(row=i, column=3)

        mask_objects.append((common_sub,name,threshold))

    pressme = Tk.Button(masks, text="Continue", command = maskthings)
    pressme.grid()
    masks.mainloop()
    print "done masks..."



    ################ Marker Options Window ###############################################

    markers = Tk.Tk()
    markers.wm_title("Marker Options")
    marker_objects = []
    # dir_list = GetPicList(basedir)

    marker_label = Tk.Label(markers, text="Marker Options")
    marker_label.grid()

    for i in range(nummarkers):
        # prefix = Tk.Entry(masks)
        # prefix.insert(0, "mask prefix")


        prefix_var = Tk.StringVar(markers)
        prefix_var.set("Choose Marker Prefix") # initial value
        prefix = apply(Tk.OptionMenu, (markers,prefix_var) + tuple(dir_list))
       
        common_sub = Tk.Entry(markers)
        common_sub.insert(0,"common subsequence")

        name = Tk.Entry(markers)
        name.insert(0, "Marker name")
        
        threshold = Tk.Entry(markers)
        threshold.insert(0, "Marker threshold")

        threshold = Tk.Scale(markers, from_=0, to=255, orient=Tk.HORIZONTAL, label="threshold", length=255)

        prefix.grid(row=i, column=0)
        common_sub.grid(row=i, column=1)
        name.grid(row=i, column=2)
        threshold.grid(row=i, column=3)

        marker_objects.append((common_sub,name,threshold))

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


    input_entry = Tk.Entry(white,width=40)
    enter_button2 = Tk.Button(white,text="Enter",command=addtowhitelistfield)

    pressme = Tk.Button(white, text="Run Analysis", command = whitelistcontinue)


    overlay_options.grid(row=0,column=0)
    enter_button.grid(row=0,column=1)
    input_entry.grid(row=1,column=0)
    enter_button2.grid(row=1,column=1)
    pressme.grid()


    white.mainloop()

    # create our configuration dict
    config_dict = createdict()

    # write it to a file in json format
    config_path = makeconfigfile(output_dir, config_dict)


    runanalysis(config_path)

    




 






