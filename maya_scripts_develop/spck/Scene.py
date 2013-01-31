# spckSetupScene.py
# Version 0.9
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

class Scene(object):
	def __init__ (self):
		pass

	def setup(self):
		'''
		Setup some scene attributes we want to be common to all Spinifex car scenes
		TODO:
		make width over height as float
		'''
		
		# Check if we haven't done this before
		if cmds.objExists('vraySettings.setupSceneHasBeenRun'):
			# Check that everything is setup correctly before continuing.
			dialogMessage = 'setupScene has already been run. Do you wish to continue? Some of your render settings will be reset.'
			result = cmds.confirmDialog( title='spckSetupScene', message=dialogMessage, button=['YES','NO'], defaultButton='NO', cancelButton='NO', dismissString='NO' )
			if result == 'NO' :
				print("Aborted. We\'ve done this before...\n")
				return
		else:
			# Check that everything is setup correctly before continuing.
			dialogMessage = 'Have you set up your workspace.mel?'
			result = cmds.confirmDialog( title='spckSetupScene', message=dialogMessage, button=['YES','NO'], defaultButton='YES', cancelButton='NO', dismissString='NO' )
			if result == 'NO' :
				print('Go setup your workspace and run again.\n')
				return
		
		# Units for working in metric and 30fps
		cmds.currentUnit (linear='cm')
		cmds.currentUnit (angle='deg')
		cmds.currentUnit (time='ntsc')

		# Load VRAY if not active
		cmds.loadPlugin ('vrayformaya', quiet=True)
		cmds.pluginInfo ('vrayformaya', edit=True, autoload=True)
		cmds.setAttr  ('defaultRenderGlobals.ren', 'vray', type='string')

		#self.createBaseRenderSettings()
		#cmds.evalDeferred ( 'self.createBaseRenderSettings()' , lowestPriority=True )	
		print('Scene Setup Success.\n')
		
	def createBaseRenderSettings(self):
		# Setup some variables
		spckDefaultWidth  = 1920
		spckDefaultHeight = 1080
		spckAspectRatio   = float(spckDefaultWidth / spckDefaultHeight)
		spckRenderPath    = '%c/%l/%c.%l'

		# Set Render Globals
		cmds.setAttr ( 'defaultRenderGlobals.currentRenderer', 'vray', type='string' )
		cmds.setAttr ( 'defaultRenderGlobals.animation', True )
		cmds.setAttr ( 'defaultResolution.width', spckDefaultWidth )
		cmds.setAttr ( 'defaultResolution.height', spckDefaultHeight )
		cmds.setAttr ( 'defaultResolution.deviceAspectRatio', spckAspectRatio )
		cmds.setAttr ( 'defaultRenderGlobals.imageFilePrefix', spckRenderPath, type='string' )

		if cmds.objExists('vraySettings'):
			# Set flag to detect that we can check later to see we've run this function
			if not cmds.objExists('vraySettings.setupSceneHasBeenRun'):
				cmds.select ( 'vraySettings' , replace = True )
				cmds.addAttr ( longName='setupSceneHasBeenRun', attributeType='message' )			

			# Set Vray Settings	
			cmds.setAttr ( 'vraySettings.aspectLock', False )
			cmds.setAttr ( 'vraySettings.animBatchOnly', True )
			cmds.setAttr ( 'vraySettings.vfbOn', True )
			cmds.setAttr ( 'vraySettings.imageFormatStr', 'exr', type='string' )
			cmds.setAttr ( 'vraySettings.imgOpt_exr_compression', 3)
			cmds.setAttr ( 'vraySettings.imgOpt_exr_bitsPerChannel', 16)
			cmds.setAttr ( 'vraySettings.imgOpt_exr_autoDataWindow', True)
			cmds.setAttr ( 'vraySettings.giOn', True )
			cmds.setAttr ( 'vraySettings.relements_separateFolders', True )
			cmds.setAttr ( 'vraySettings.width', spckDefaultWidth )
			cmds.setAttr ( 'vraySettings.height', spckDefaultHeight )
			cmds.setAttr ( 'vraySettings.samplerType', 2 )
			cmds.setAttr ( 'vraySettings.sys_low_thread_priority', True )
			cmds.setAttr ( 'vraySettings.aspectRatio', spckAspectRatio )
			cmds.setAttr ( 'vraySettings.aaFilterType', 6)
			cmds.setAttr ( 'vraySettings.aaFilterSize', 2.5)
			cmds.setAttr ( 'vraySettings.dmcs_adaptiveAmount', 0.85) # Rob N is 0.9, roy likes 0.85
			cmds.setAttr ( 'vraySettings.sys_rayc_dynMemLimit', 8000) 
			cmds.setAttr ( 'vraySettings.fileNamePrefix', spckRenderPath, type='string' )
			cmds.setAttr ( 'vraySettings.dontSaveImage', True )
			cmds.setAttr ( 'vraySettings.sys_regsgen_xc', 32 )
				
			# Setup Linear Workflow
			cmds.setAttr ( 'vraySettings.cmap_linearworkflow', False )
			cmds.setAttr ( 'vraySettings.cmap_adaptationOnly', True )
			cmds.setAttr ( 'vraySettings.cmap_gamma', 2.2 )
			cmds.setAttr ( 'vraySettings.sRGBOn', True )
			cmds.setAttr ( 'vraySettings.cmap_affectBackground', True )
			cmds.setAttr ( 'vraySettings.cmap_affectSwatches', True )
		
			# Setup Roy-defaults
			cmds.setAttr ( 'vraySettings.samplerType', 1 )
			cmds.setAttr ( 'vraySettings.aaFilterType', 6 )
			cmds.setAttr ( 'vraySettings.cmap_subpixelMapping', False )
			cmds.setAttr ( 'vraySettings.refractiveCaustics', 0 )
			cmds.setAttr ( 'vraySettings.primaryMultiplier', 1.0 )
			cmds.setAttr ( 'vraySettings.secondaryEngine', 3 )
			cmds.setAttr ( 'vraySettings.secondaryMultiplier', 1.0 )
			cmds.setAttr ( 'vraySettings.imap_currentPreset', 0 )
			cmds.setAttr ( 'vraySettings.imap_minRate', -3 )
			cmds.setAttr ( 'vraySettings.imap_maxRate', -2 )
			cmds.setAttr ( 'vraySettings.imap_subdivs', 80 )
			cmds.setAttr ( 'vraySettings.imap_interpSamples', 25 )
			cmds.setAttr ( 'vraySettings.imap_detailEnhancement', True )
			cmds.setAttr ( 'vraySettings.imap_detailScale', True )
			cmds.setAttr ( 'vraySettings.imap_detailRadius', 20 )
			cmds.setAttr ( 'vraySettings.imap_detailSubdivsMult', 0.2 )
			cmds.setAttr ( 'vraySettings.imap_calcInterpSamples', 15 )
			cmds.setAttr ( 'vraySettings.numPasses', 20 )
			cmds.setAttr ( 'vraySettings.prefilter', True )
			cmds.setAttr ( 'vraySettings.useForGlossy', True )
			cmds.setAttr ( 'vraySettings.useRetraceThreshold', True )
			cmds.setAttr ( 'vraySettings.ddisplac_maxSubdivs', 8 )
		
			cmds.select( clear=True)
			print('setBaseRenderSettings Success.\n')