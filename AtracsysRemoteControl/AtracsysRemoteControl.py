import os
import unittest
import vtk, qt, ctk, slicer
import xml.etree.ElementTree as xml
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
    self.connectorNodeObserverTagList = []
    self.logic = AtracsysRemoteControlLogic()

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/AtracsysRemoteControl.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    self.ui.connectorNodeSelector.setMRMLScene(slicer.mrmlScene)
    
    # signal-slot connections
    self.ui.connectorNodeSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onConnectorNodeSelected)
    self.ui.deviceComboBox.connect('currentIndexChanged(int)', self.onDeviceIDChanged)

    self.ui.ledEnableCheckBox.connect('stateChanged(int)', self.onLedEnableChecked)
    self.ui.redSlider.connect('valueChanged(double)', self.onLedRedValueChanged)
    self.ui.greenSlider.connect('valueChanged(double)', self.onLedBlueValueChanged)
    self.ui.blueSlider.connect('valueChanged(double)', self.onLedBlueValueChanged)
    self.ui.frequencySlider.connect('valueChanged(double)', self.onLedFrequencyValueChanged)

    self.ui.markerComboBox.connect('currentIndexChanged(int)', self.onMarkerComboBoxSelectedChanged)
    self.ui.markerEnableButton.connect('clicked(bool)', self.onMarkerEnableButtonPressed)
    self.ui.markerPathLineEdit.connect('currentPathChanged(QString&)', self.onMarkerGeometryFileSelectorModified)
    self.ui.markerAddButton.connect('clicked(bool)', self.onMarkerAddButtonPressed)

    self.ui.laserEnableCheckBox.connect('stateChanged(int)', self.onLaserEnableChecked)
    self.ui.videoEnableCheckBox.connect('stateChanged(int)', self.onVideoEnableChecked)

    self.plusRemoteNode = slicer.mrmlScene.GetFirstNodeByClass('vtkMRMLPlusRemoteNode')
    if self.plusRemoteNode is None:
      self.plusRemoteNode = slicer.vtkMRMLPlusRemoteNode()
      self.plusRemoteNode.SetName("PlusRemoteNode")
      slicer.mrmlScene.AddNode(self.plusRemoteNode)
    self.plusRemoteNode.AddObserver(slicer.vtkMRMLPlusRemoteNode.DeviceIdsReceivedEvent, self.requestDeviceIDsCompleted)
    self.onConnectorNodeSelected(self.ui.connectorNodeSelector.currentNode())

    
  def onReload(self):
    pass


  def requestDeviceIDsCompleted(self, object=None, event=None, caller=None):
    wasBlocked = self.ui.deviceComboBox.blockSignals(True)
    self.ui.deviceComboBox.clear()
    deviceIDs = vtk.vtkStringArray()
    self.plusRemoteNode.GetDeviceIDs(deviceIDs)
    currentDeviceID = self.plusRemoteNode.GetCurrentDeviceID()

    for valueIndex in range(deviceIDs.GetNumberOfValues()):
      deviceID = deviceIDs.GetValue(valueIndex)
      self.ui.deviceComboBox.addItem(deviceID)

    currentIndex = self.ui.deviceComboBox.findText(currentDeviceID)
    self.ui.deviceComboBox.setCurrentIndex(currentIndex)
    self.ui.deviceComboBox.blockSignals(wasBlocked)
    self.onDeviceIDChanged()


  def onConnectorNodeSelected(self, connectorNode):
    for obj, tag in self.connectorNodeObserverTagList:
      obj.RemoveObserver(tag)
    self.connectorNodeObserverTagList = []

    # Add observers for connect/disconnect events
    if connectorNode is not None:
      events = [[slicer.vtkMRMLIGTLConnectorNode.ConnectedEvent, self.onConnectorNodeConnectionChanged], [slicer.vtkMRMLIGTLConnectorNode.DisconnectedEvent, self.onConnectorNodeConnectionChanged]]
      for tagEventHandler in events:
        connectorNodeObserverTag = connectorNode.AddObserver(tagEventHandler[0], tagEventHandler[1])
        self.connectorNodeObserverTagList.append((connectorNode, connectorNodeObserverTag))

    self.plusRemoteNode.SetAndObserveOpenIGTLinkConnectorNode(connectorNode)
    self.logic.setConnectorNode(connectorNode)


    self.onConnectorNodeConnectionChanged()

  def onConnectorNodeConnectionChanged(self, object=None, event=None, caller=None):
    connectorNode = self.ui.connectorNodeSelector.currentNode()
    if (connectorNode is not None and connectorNode.GetState() == slicer.vtkMRMLIGTLConnectorNode.StateConnected):
      self.plusRemoteNode.SetDeviceIDType("")
      slicer.modules.plusremote.logic().RequestDeviceIDs(self.plusRemoteNode)

  def onDeviceIDChanged(self):
    currentDeviceID = self.ui.deviceComboBox.currentText
    self.plusRemoteNode.SetCurrentDeviceID(currentDeviceID)
    self.logic.setDeviceID(currentDeviceID)


  def onLedEnableChecked(self):
    commandName = "LedEnabled"
    if self.ui.ledEnableCheckBox.isChecked():
      value = "TRUE"
    else:
      value = "FALSE"
    self.logic.setParameter(commandName, value)


  def onLedRedValueChanged(self):
    #commandName = 
    print("red")


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

  def setConnectorNode(self, connectorNode):
    self.connectorNode = connectorNode


  def setDeviceID(self, deviceID):
    self.deviceID = deviceID


  def setParameter(self, parameterName, value):
    command = slicer.vtkSlicerOpenIGTLinkCommand()

    content = xml.Element('Command')
    content.attrib = {
        'Name':'AtracsysCommand',
        'DeviceID':'TrackerDevice'
      }
    body = xml.SubElement(content, 'SetParameter')
    body.attrib = {
      'Name':'LedEnabled',
      'Value':'FALSE'
      }

    command.SetCommandContent(xml.tostring(content))
    command.SendCommand(self.connectorNode)


  def getParameter(self, parameterName):
    pass




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
