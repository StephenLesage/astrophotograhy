#!/usr/bin/python
import subprocess
import time
import sys
import os
import re

# Prompt user to input the specific object and exposure time to be processed
image_content = ""
while not (len(image_content)>0 and re.match("^(?!_)\w*(?<!_)$",image_content)):
    image_content = raw_input('\nWhat are you imaging? (Ex: jupiter, moon, m31...)\n'+
                'Please use only alphanumeric characters (a-z,0-9)\n')
    image_exposure = raw_input('\nWhat is the exposure? (Ex: 500ms, 4s)\n'+
                'Please use only alphanumeric characters (a-z,0-9)\n')
dir_name = (time.strftime("%Y%m%d"))+'_'+image_content

# Check if data directory exists, if it doesn't, make it
if not os.path.isdir(str("data/")):
    subprocess.call("mkdir data/", shell=True)

# Check if user-specific data directories exist, if they don't, make them
if not os.path.isdir(str("data/"+dir_name+"/"+image_exposure)):
    if not os.path.isdir(str("data/"+dir_name)):
        subprocess.call("mkdir data/"+dir_name, shell=True)
    subprocess.call("mkdir data/"+dir_name+"/"+image_exposure, shell=True)
    sub_directories = ['infrared', 'red', 'green', 'blue', 'visible', 'solar', 'darks', 'flats']
    for sub_dir in sub_directories:
        subprocess.call("mkdir data/"+dir_name+"/"+image_exposure+"/"+sub_dir, shell=True)
else:
    sys.exit(dir_name+" already exists as a directory")

# Prompt user about next steps
Print('\nYour data directories have been created.\n'+
    'Please fill them with your images.\n')