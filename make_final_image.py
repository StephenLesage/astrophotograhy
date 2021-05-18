import os
import subprocess
import numpy as np
from astropy.io import fits
import pylab as py
import matplotlib.pyplot as plt

def Median_Combine_Darks( filepath ):

	# Update filepath
	filepath = filepath + 'darks/'
	print( 'Working on darks' )

	# Finding all dark images
	darks = {}
	file_num = 0
	for filename in os.listdir(filepath):
		if filename.endswith(".fit"): 
			#print 'found image at ' + filepath + filename
			darks[file_num] = fits.open(filepath+filename)[0].data
			file_num += 1
		else:
			print(filename + ' is not a valid image file')

	# Stack dark image numpy arrays 
	darks_stack = []
	x = 0
	for x in range( file_num - 1 ):
		darks_stack.append(darks[x])
	
	# Median combine all dark images into a final image
	final_darks = np.median(darks_stack, axis=0)
	
	return final_darks

def Align_RGB_Filter_Images( filepath, final_darks, red = None, green = None, blue = None, show_every_image = None, show_final_image = None ):

	# Update filepath
	if red != None:
		filepath = filepath + 'red/'
		print( 'Working on red filter' )
	if green != None:
		filepath = filepath + 'green/'
		print( 'Working on green filter' )
	if blue != None:
		filepath = filepath + 'blue/'
		print( 'Working on blue filter' )

	# Finding all filter images
	image = {}
	file_num = 0
	for filename in os.listdir(filepath):
	    if filename.endswith(".fit"): 
	        #print 'found image at ' + filepath + filename
	        image[ file_num ] = fits.open( filepath + filename )[0].data
	        file_num += 1
	    else:
	    	print(filename + ' is not a valid image file')

	# Subtract darks from numpy arrays
	x = 0
	for x in range( file_num - 1 ):
		image[x] = (image[x] - final_darks)
		if show_every_image != None:
			if red != None:
				plt.imshow(final_green_image, cmap='Reds')
			if green != None:
				plt.imshow(final_green_image, cmap='Greens')
			if blue != None:
				plt.imshow(final_green_image, cmap='Blues')
			plt.colorbar()
			plt.show()
	
	# Squishes each image into a 1D column array and finds where the max value is (vertical)
	indexcolumnarray = []
	x = 0
	for x in range( file_num - 1 ):
		column = []
		for i in range(1024):
			y=0
			for j in range(1360):
				y += image[x][i][j]
			column.append(y)
		index = np.where(column == np.max(column))
		indexcolumnarray.append(index[0][0])
	
	# Squishes each image into a 1D row array and finds where the max value is (horizontal)
	indexrowarray = []
	x = 0
	for x in range( file_num - 1 ):
		row = []
		for i in range(1360):
			y=0
			for j in range(1024):
				y += image[x][j][i]
			row.append(y)
		index = np.where(row == np.max(row))
		indexrowarray.append(index[0][0])
	
	# Shift images vertically
	vertical_shifted = []
	x = 0
	for x in range( file_num - 1 ):
		image[x] = np.roll(image[x], (indexcolumnarray[0] - indexcolumnarray[x]), axis=0)
		vertical_shifted.append(image[x])
	
	# Shift images horizontally
	final_shifted = []
	x = 0
	for x in range( file_num - 1 ):
		vertical_shifted[x] = np.roll(vertical_shifted[x], (indexrowarray[0] - indexrowarray[x]), axis=1)
		final_shifted.append(vertical_shifted[x])
	
	# Median combine all shifted images into a final image
	final_image = np.median(final_shifted, axis=0)
	
	# Display final median combined numpy array
	if show_final_image != None:
		if red != None:
			plt.imshow(final_green_image, cmap='Reds')
		if green != None:
			plt.imshow(final_green_image, cmap='Greens')
		if blue != None:
			plt.imshow(final_green_image, cmap='Blues')
		plt.colorbar()
		plt.show()

	return final_image

def Final_RGB_Image( final_red_image, final_green_image, final_blue_image ):

	print( 'Working on final image' )

	# Combine all filter images into one array
	rgb_image = [final_red_image, final_green_image, final_blue_image]

	# Squishes each jupiter image into a 1D column array and finds where the max value is (vertical)
	indexcolumnarray = []
	x = 0
	for x in range(3):
		rgb_column = []
		for i in range(1024):
			y=0
			for j in range(1360):
				y += rgb_image[x][i][j]
			rgb_column.append(y)
		index = np.where(rgb_column == np.max(rgb_column))
		indexcolumnarray.append(index[0][0])
	
	# Squishes each jupiter image into a 1D row array and finds where the max value is (horizontal)
	indexrowarray = []
	x = 0
	for x in range(3):
		rgb_row = []
		for i in range(1360):
			y=0
			for j in range(1024):
				y += rgb_image[x][j][i]
			rgb_row.append(y)
		index = np.where(rgb_row == np.max(rgb_row))
		indexrowarray.append(index[0][0])
	
	# Shift images vertically
	rgb_vertical_shifted = []
	x = 0
	for x in range(3):
		rgb_image[x] = np.roll(rgb_image[x], (indexcolumnarray[0] - indexcolumnarray[x]), axis=0)
		rgb_vertical_shifted.append(rgb_image[x])
	
	# Shift images horizontally
	rgb_final_shifted = []
	x = 0
	for x in range(3):
		rgb_vertical_shifted[x] = np.roll(rgb_vertical_shifted[x], (indexrowarray[0] - indexrowarray[x]), axis=1)
		rgb_final_shifted.append(rgb_vertical_shifted[x])

	# Jupiter
	# Creating a proper rgb image
	rgb_final_shifted[0] = (rgb_final_shifted[0]/(65536))
	rgb_final_shifted[1] = (rgb_final_shifted[1]/(65536))
	rgb_final_shifted[2] = (rgb_final_shifted[2]/(65536))
	# Saturn
	# Creating a proper rgb image
#	rgb_final_shifted[0] = (rgb_final_shifted[0]/(1000))
#	rgb_final_shifted[1] = (rgb_final_shifted[1]/(1000))
#	rgb_final_shifted[2] = (rgb_final_shifted[2]/(1000))
	# Venus
	# Creating a proper rgb image
#	rgb_final_shifted[0] = (rgb_final_shifted[0]/(5000))
#	rgb_final_shifted[1] = (rgb_final_shifted[1]/(5000))
#	rgb_final_shifted[2] = (rgb_final_shifted[2]/(5000))
	# Jupiter's Moons
	# Creating a proper rgb image and blocks out jupiter so you can see the moons
#	for i in range(1360):
#		y = 0
#		for j in range(1024):
#			y = rgb_final_shifted[0][j][i]
#			if y > 5000.0:
#				y = 2000.0
#			rgb_final_shifted[0][j][i] = y
#	for i in range(1360):
#		y = 0
#		for j in range(1024):
#			y = rgb_final_shifted[1][j][i]
#			if y > 5000.0:
#				y = 2000.0
#			rgb_final_shifted[1][j][i] = y
#	for i in range(1360):
#		y = 0
#		for j in range(1024):
#			y = rgb_final_shifted[2][j][i]
#			if y > 5000.0:
#				y = 2000.0
#			rgb_final_shifted[2][j][i] = y
#	rgb_final_shifted[0] = (rgb_final_shifted[0]/(5000))
#	rgb_final_shifted[1] = (rgb_final_shifted[1]/(5000))
#	rgb_final_shifted[2] = (rgb_final_shifted[2]/(5000))

	# Fill numpy array with RGB values
	rgbArray = np.zeros((1024,1360,3))
	rgbArray[..., 0] = rgb_final_shifted[0]
	rgbArray[..., 1] = rgb_final_shifted[1]
	rgbArray[..., 2] = rgb_final_shifted[2]

	return rgbArray

def Final_Visible_Image( filepath, final_darks, show_every_image = None ):

	# Update filepath
	filepath = filepath + 'visible/'
	print( 'Working on visible images' )

	# Finding all visible images
	visible_image = {}
	file_num = 0
	for filename in os.listdir(filepath):
	    if filename.endswith(".fit"): 
	        #print 'found image at ' + filepath + filename
	        visible_image[file_num] = fits.open(filepath+filename)[0].data
	        file_num+=1
	    else:
	    	print filename + ' is not a valid image file'

	# Subtract darks from numpy arrays and view images
	x = 0
	for x in range( file_num - 1 ):
		visible_image[x] = (visible_image[x] - final_darks)
		if show_every_image != None:
			plt.imshow(visible_image[x], cmap='Greys')
			plt.colorbar()
			plt.show()

	# Squishes each image into a 1D column array and finds where the max value is (vertical)
	indexcolumnarray = []
	x = 0
	for x in range( file_num - 1 ):
		visible_column = []
		for i in range(1024):
			y=0
			for j in range(1360):
				y += visible_image[x][i][j]
			visible_column.append(y)
		index = np.where(visible_column == np.max(visible_column))
		indexcolumnarray.append(index[0][0])
	
	# Squishes each image into a 1D row array and finds where the max value is (horizontal)
	indexrowarray = []
	x = 0
	for x in range( file_num - 1 ):
		visible_row = []
		for i in range(1360):
			y=0
			for j in range(1024):
				y += visible_image[x][j][i]
			visible_row.append(y)
		index = np.where(visible_row == np.max(visible_row))
		indexrowarray.append(index[0][0])
	
	# Shift images vertically
	visible_vertical_shifted = []
	x = 0
	for x in range( file_num - 1 ):
		visible_image[x] = np.roll(visible_image[x], (indexcolumnarray[0] - indexcolumnarray[x]), axis=0)
		visible_vertical_shifted.append(visible_image[x])
	
	# Shift images horizontally
	visible_final_shifted = []
	x = 0
	for x in range( file_num - 1 ):
		visible_vertical_shifted[x] = np.roll(visible_vertical_shifted[x], (indexrowarray[0] - indexrowarray[x]), axis=1)
		visible_final_shifted.append(visible_vertical_shifted[x])
	
	# Median combine all shifted images into a final image
	final_visible_image = np.median(visible_final_shifted, axis=0)

	return final_visible_image

def Plot_Final_Image( filepath, final_image_array, RGB = None, visible = None ):

	# Check if data directory exists, if it doesn't, make it
	if not os.path.isdir(str("final_image/")):
		subprocess.call("mkdir final_image/", shell=True)

	# Create and save RGB image
	if RGB != None:
		py.clf
		py.imshow(final_image_array, aspect='equal')
		filepath_parts = filepath.split('/')
		for i in range(len(filepath_parts)):
			if '_' in filepath_parts[i]:
				date_string = filepath_parts[i].split('_')[0]
				try:
					name_string = filepath_parts[i].split('_')[1] + '_' + filepath_parts[i].split('_')[2]
				except:
					name_string = filepath_parts[i].split('_')[1]
		py.title(name_string+'_'+date_string)
		py.savefig('final_image/' + name_string + '.png')

	# Create and save visible image
	if visible != None:
		filepath_parts = filepath.split('/')
		for i in range(len(filepath_parts)):
			if '_' in filepath_parts[i]:
				date_string = filepath_parts[i].split('_')[0]
				try:
					name_string = filepath_parts[i].split('_')[1] + '_' + filepath_parts[i].split('_')[2]
				except:
					name_string = filepath_parts[i].split('_')[1]
		plt.clf()
		plt.imshow(final_visible_image, cmap='Greys')
		plt.title(name_string+'_'+date_string)
		plt.savefig('final_image/' + name_string + '_greyscale.png')
		plt.clf()
		plt.imshow(final_visible_image)
		plt.title(name_string+'_'+date_string)
		plt.savefig('/final_image/' + name_string + '_falsecolor.png')


	return

##############################
############ MAIN ############
##############################

RGB = True
filepath = 'data/20170510_jupiter/100ms/'
#filepath = 'data/20170613_saturn/19ms/'
#filepath = 'data/20170613_venus/3ms/'
#filepath = 'data/20170510_jupiter_moons/250ms/'
#visible = True
#filepath = 'data/20170613_saturn/19ms/'
#filepath = 'data/20170613_venus/3ms/'

try:
	if RGB == True:
		# Median combine all dark images into a final image
		final_darks = Median_Combine_Darks( filepath )
		# Median combine all shifted filter images into final images
		final_red_image = Align_RGB_Filter_Images( filepath, final_darks, red = True )
		final_green_image = Align_RGB_Filter_Images( filepath, final_darks, green = True )
		final_blue_image = Align_RGB_Filter_Images( filepath, final_darks, blue = True )
		# Shift and combine all filtered images into a final image
		final_visible_image = Final_RGB_Image( final_red_image, final_green_image, final_blue_image )
		# Genenerate and save final image
		Plot_Final_Image( filepath, final_visible_image, RGB = True )
except:
	NameError

try:
	if visible == True:
		# Median combine all dark images into a final image
		final_darks = Median_Combine_Darks( filepath )
		# Shift and combine all filtered images into a final image
		final_visible_image = Final_Visible_Image( filepath, final_darks )
		# Genenerate and save final image
		Plot_Final_Image( filepath, final_visible_image, visible = True )
except:
	NameError





