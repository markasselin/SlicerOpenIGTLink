/*==============================================================================

  Program: 3D Slicer

  Portions (c) Copyright Brigham and Women's Hospital (BWH) All Rights Reserved.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

==============================================================================*/

// TrackerRemoteControl Logic includes
#include <vtkSlicerTrackerRemoteControlLogic.h>

// TrackerRemoteControl includes
#include "qSlicerTrackerRemoteControlModule.h"
#include "qSlicerTrackerRemoteControlModuleWidget.h"

//-----------------------------------------------------------------------------
#if (QT_VERSION < QT_VERSION_CHECK(5, 0, 0))
#include <QtPlugin>
Q_EXPORT_PLUGIN2(qSlicerTrackerRemoteControlModule, qSlicerTrackerRemoteControlModule);
#endif

//-----------------------------------------------------------------------------
/// \ingroup Slicer_QtModules_ExtensionTemplate
class qSlicerTrackerRemoteControlModulePrivate
{
public:
  qSlicerTrackerRemoteControlModulePrivate();
};

//-----------------------------------------------------------------------------
// qSlicerTrackerRemoteControlModulePrivate methods

//-----------------------------------------------------------------------------
qSlicerTrackerRemoteControlModulePrivate::qSlicerTrackerRemoteControlModulePrivate()
{
}

//-----------------------------------------------------------------------------
// qSlicerTrackerRemoteControlModule methods

//-----------------------------------------------------------------------------
qSlicerTrackerRemoteControlModule::qSlicerTrackerRemoteControlModule(QObject* _parent)
  : Superclass(_parent)
  , d_ptr(new qSlicerTrackerRemoteControlModulePrivate)
{
}

//-----------------------------------------------------------------------------
qSlicerTrackerRemoteControlModule::~qSlicerTrackerRemoteControlModule()
{
}

//-----------------------------------------------------------------------------
QString qSlicerTrackerRemoteControlModule::helpText() const
{
  return "This extension provides the ability to control some PLUS compatible trackers over OpenIGTLink.";
}

//-----------------------------------------------------------------------------
QString qSlicerTrackerRemoteControlModule::acknowledgementText() const
{
  return "This work was partially funded by NIH grant NXNNXXNNNNNN-NNXN";
}

//-----------------------------------------------------------------------------
QStringList qSlicerTrackerRemoteControlModule::contributors() const
{
  QStringList moduleContributors;
  moduleContributors << QString("Mark Asselin (Perk Lab, Queen's University)");
  return moduleContributors;
}

//-----------------------------------------------------------------------------
QIcon qSlicerTrackerRemoteControlModule::icon() const
{
  return QIcon(":/Icons/TrackerRemoteControl.png");
}

//-----------------------------------------------------------------------------
QStringList qSlicerTrackerRemoteControlModule::categories() const
{
  return QStringList() << "IGT";
}

//-----------------------------------------------------------------------------
QStringList qSlicerTrackerRemoteControlModule::dependencies() const
{
  return QStringList();
}

//-----------------------------------------------------------------------------
void qSlicerTrackerRemoteControlModule::setup()
{
  this->Superclass::setup();
}

//-----------------------------------------------------------------------------
qSlicerAbstractModuleRepresentation* qSlicerTrackerRemoteControlModule
::createWidgetRepresentation()
{
  return new qSlicerTrackerRemoteControlModuleWidget;
}

//-----------------------------------------------------------------------------
vtkMRMLAbstractLogic* qSlicerTrackerRemoteControlModule::createLogic()
{
  return vtkSlicerTrackerRemoteControlLogic::New();
}
