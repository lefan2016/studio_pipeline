#!/usr/bin/python
#spck_aepx_maker.py
#
#Takes template spck .aepx file and changes all expressions and composition names to new shot name

import binascii
import re
import os
import sys

def spckProcessTemplateAepxFile (replacementSceneNumber, replacementShotNumber, camWidth, camHeight, exchangePath, renderPath, renderSceneName, renderCameraName):
	
	spckVersion				  = 'v0.3'
	templateSceneName		  = 'vray_shaders_dan'
	templateShotName		  = 'shXXXX'
	templateFileLocation	  = '/Volumes/RESOURCES/05_Motion_Studio_Tools/spck/aepx/spck_'+spckVersion+'_shXXXX.aepx'
	templateRenderPath		  = '/Volumes/RED/01_Production/INTE1312_Spinifex_Perfect_Car_Kit/3_Studio/d_3D/Renders/vray_shaders_dan/camera_wide_car_framed_right/'
	templaterenderCameraName  = 'camera_wide_car_framed_right'
	
	#replacementSceneNumber = str(input('New Shot Name (characters and numbers and underscore only - no spaces - enlose in single quotes): '))
	replacementShotPath = exchangePath+'spck_'+spckVersion+'_sc'+replacementSceneNumber+'_sh'+replacementShotNumber+'_v001.aepx'

	#expand tilde if writing to user directory
	if '~' in replacementShotPath:
		replacementShotPath = os.path.expanduser(replacementShotPath)
	
	fileIn  = open(templateFileLocation)
	fileOut = open(replacementShotPath, "wt")
	
	#change replacement shot name because using non-shXXXX format is going to break the AE file
	replacementSceneNumber		= 'sh'+replacementShotNumber
	
	for line in fileIn:
		# for each line in file, search for the shot name and replace with new shot name
		# some of the shot names are hidden in binary data in bdata = "hex data" lines
		# if no shot name found in line, write out original line
		
		if templateShotName in line:
			fileOut.write( line.replace(templateShotName, replacementSceneNumber))
			#print line
		elif templateRenderPath in line:
			fileOut.write( line.replace(templateRenderPath, renderPath))

		elif 'bdata' in line:
			#for each bdata line, find the binary data between the quotes, and unhex it
			#strip the quotes "" from the extracted data
			#search for the shot name and replace if found
			#write out new line if data was replaced otherwise write out old line
			
			bData = re.search (r'"(.*?)"' , line)
			bDataNoQuotes = bData.group(0).replace('"', '').strip()
			asciiData = binascii.unhexlify(bDataNoQuotes)
			if templateShotName in asciiData:
				asciiData = asciiData.replace (templateShotName, replacementSceneNumber)
				replacementData = binascii.hexlify(asciiData)
				line = line.replace(bDataNoQuotes, replacementData)
			elif templaterenderCameraName in asciiData:
				asciiData = asciiData.replace (templaterenderCameraName, renderCameraName)
				replacementData = binascii.hexlify(asciiData)
				line = line.replace(bDataNoQuotes, replacementData)
			elif templateSceneName in asciiData:
				asciiData = asciiData.replace (templateSceneName, renderSceneName)
				replacementData = binascii.hexlify(asciiData)
				line = line.replace(bDataNoQuotes, replacementData)
			fileOut.write(line)
		else:
			fileOut.write(line)
			
	#Be nice and close the files
	
	fileIn.close()
	fileOut.close()