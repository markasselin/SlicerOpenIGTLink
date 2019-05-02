import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# AtracsysRemoteControl
#

class AtracsysRemoteControl(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "AtracsysRemoteControl"
    self.parent.categories = ["IGT"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mark Asselin (Perk Lab, Queen's University)"]
    self.parent.helpText = """
This module allows the remote control of an Atracsys tracker.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This work was funded, in part, by NIH/NIBIB and NIH/NIGMS (via grant 1R01EB021396-01A1 - Slicer+PLUS: 
Point-of-Care Ultrasound) and by CANARIE's Research Software Program.
"""

#
# AtracsysRemoteControlWidget
#

class AtracsysRemoteControlWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/AtracsysRemoteControl.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    self.ui.qMRMLNodeComboBox.setMRMLScne(slicer.mrmlScene)


    # connections
    self.ui.plusNodeComboBox.connect('currentNodeChanged(vtkMRMLNode*)', self.onPlusNodeChanged)



    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)


    # Add vertical spacer
    self.layout.addStretch(1)



  def onPlusNodeChanged(self):
    pass

  
  def onDeviceSelected(self):
    pass


  def onLedEnableChecked(self):
    pass


  def onLedRedValueChanged(self):
    pass


  def onLedGreenValueChanged(self):
    pass


  def onLedBlueValueChanged(self):
    pass


  def onLedFrequencyValueChanged(self):
    pass


  def onMarkerComboBoxSelectedChanged(self):
    pass


  def onMarkerEnableButtonPressed(self):
    pass


  def onMarkerGeometryFileSelectorModified(self):
    pass


  def onMarkerAddButtonPressed(self):
    pass


  def onLaserEnableChecked(self):
    pass


  def onVideoEnableChecked(self):
    pass


  def cleanup(self):
    pass



  def onApplyButton(self):
    logic = AtracsysRemoteControlLogic()
    enableScreenshotsFlag = self.ui.enableScreenshotsFlagCheckBox.checked
    imageThreshold = self.ui.imageThresholdSliderWidget.value
    logic.run(self.ui.inputSelector.currentNode(), self.ui.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)

#
# AtracsysRemoteControlLogic
#

class AtracsysRemoteControlLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('AtracsysRemoteControlTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class AtracsysRemoteControlTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_AtracsysRemoteControl1()

  def test_AtracsysRemoteControl1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = AtracsysRemoteControlLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
