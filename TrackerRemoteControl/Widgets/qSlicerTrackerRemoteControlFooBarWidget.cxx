/*==============================================================================

  Program: 3D Slicer

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// FooBar Widgets includes
#include "qSlicerTrackerRemoteControlFooBarWidget.h"
#include "ui_qSlicerTrackerRemoteControlFooBarWidget.h"

//-----------------------------------------------------------------------------
/// \ingroup Slicer_QtModules_TrackerRemoteControl
class qSlicerTrackerRemoteControlFooBarWidgetPrivate
  : public Ui_qSlicerTrackerRemoteControlFooBarWidget
{
  Q_DECLARE_PUBLIC(qSlicerTrackerRemoteControlFooBarWidget);
protected:
  qSlicerTrackerRemoteControlFooBarWidget* const q_ptr;

public:
  qSlicerTrackerRemoteControlFooBarWidgetPrivate(
    qSlicerTrackerRemoteControlFooBarWidget& object);
  virtual void setupUi(qSlicerTrackerRemoteControlFooBarWidget*);
};

// --------------------------------------------------------------------------
qSlicerTrackerRemoteControlFooBarWidgetPrivate
::qSlicerTrackerRemoteControlFooBarWidgetPrivate(
  qSlicerTrackerRemoteControlFooBarWidget& object)
  : q_ptr(&object)
{
}

// --------------------------------------------------------------------------
void qSlicerTrackerRemoteControlFooBarWidgetPrivate
::setupUi(qSlicerTrackerRemoteControlFooBarWidget* widget)
{
  this->Ui_qSlicerTrackerRemoteControlFooBarWidget::setupUi(widget);
}

//-----------------------------------------------------------------------------
// qSlicerTrackerRemoteControlFooBarWidget methods

//-----------------------------------------------------------------------------
qSlicerTrackerRemoteControlFooBarWidget
::qSlicerTrackerRemoteControlFooBarWidget(QWidget* parentWidget)
  : Superclass( parentWidget )
  , d_ptr( new qSlicerTrackerRemoteControlFooBarWidgetPrivate(*this) )
{
  Q_D(qSlicerTrackerRemoteControlFooBarWidget);
  d->setupUi(this);
}

//-----------------------------------------------------------------------------
qSlicerTrackerRemoteControlFooBarWidget
::~qSlicerTrackerRemoteControlFooBarWidget()
{
}
