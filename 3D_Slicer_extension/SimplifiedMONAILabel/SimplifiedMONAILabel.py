# Copyright © 2024 Brayan Daniel Oviedo
# Modified from MONAI Label project, available at https://github.com/Project-MONAI/MONAILabel
# Licensed under the Apache License, Version 2.0
# See LICENSE file in the project root for license information.

import json
import logging
import os
import shutil
import tempfile
import time
import traceback
from collections import OrderedDict
from urllib.parse import quote_plus

import ctk
import qt
import SampleData
import SimpleITK as sitk
import sitkUtils
import slicer
import vtk
import vtkSegmentationCore
from MONAILabelLib import GenericAnatomyColors, MONAILabelClient
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


class SimplifiedMONAILabel(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("SimplifiedMONAILabel")
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Segmentation")]
        self.parent.dependencies = []
        self.parent.contributors = ["Universidad de Antioquia"]
        self.parent.helpText = _(
            """
Simplified version of an existing extension from MONAI Label.
See more information in <a href="https://github.com/Project-MONAI/MONAILabel">module documentation</a>.
"""
        )
        self.parent.acknowledgementText = _(
            """
This work was for a internship project from Universidad de Antioquia
"""
        )

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", self.initializeAfterStartup)

    def initializeAfterStartup(self):
        if not slicer.app.commandOptions().noMainWindow:
            self.settingsPanel = SimplifiedMONAILabelSettingsPanel()
            slicer.app.settingsDialog().addPanel("MONAI Label", self.settingsPanel)


class _ui_SimplifiedMONAILabelSettingsPanel:
    def __init__(self, parent):
        vBoxLayout = qt.QVBoxLayout(parent)

        # settings
        groupBox = ctk.ctkCollapsibleGroupBox()
        groupBox.title = _("MONAI Label Server")
        groupLayout = qt.QFormLayout(groupBox)

        serverUrl = qt.QLineEdit()
        groupLayout.addRow(_("Server address:"), serverUrl)
        parent.registerProperty("MONAILabel/serverUrl", serverUrl, "text", str(qt.SIGNAL("textChanged(QString)")))

        serverUrlHistory = qt.QLineEdit()
        groupLayout.addRow(_("Server address history:"), serverUrlHistory)
        parent.registerProperty(
            "MONAILabel/serverUrlHistory", serverUrlHistory, "text", str(qt.SIGNAL("textChanged(QString)"))
        )

        fileExtension = qt.QLineEdit()
        fileExtension.setText(".nii.gz")
        fileExtension.toolTip = _("Default extension for uploading images/labels")
        groupLayout.addRow(_("File Extension:"), fileExtension)
        parent.registerProperty(
            "MONAILabel/fileExtension", fileExtension, "text", str(qt.SIGNAL("textChanged(QString)"))
        )

        clientId = qt.QLineEdit()
        clientId.setText(_("user-xyz"))
        clientId.toolTip = _("Client/User ID that will be sent to MONAI Label server for reference")
        groupLayout.addRow(_("Client/User-ID:"), clientId)
        parent.registerProperty("MONAILabel/clientId", clientId, "text", str(qt.SIGNAL("textChanged(QString)")))

        autoRunSegmentationCheckBox = qt.QCheckBox()
        autoRunSegmentationCheckBox.checked = False
        autoRunSegmentationCheckBox.toolTip = _(
            "Enable this option to auto run segmentation if pre-trained model exists when Next Sample is fetched"
        )
        groupLayout.addRow(_("Auto-Run Pre-Trained Model:"), autoRunSegmentationCheckBox)
        parent.registerProperty(
            "MONAILabel/autoRunSegmentationOnNextSample",
            ctk.ctkBooleanMapper(autoRunSegmentationCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        autoFetchNextSampleCheckBox = qt.QCheckBox()
        autoFetchNextSampleCheckBox.checked = False
        autoFetchNextSampleCheckBox.toolTip = _("Enable this option to fetch Next Sample after saving the label")
        groupLayout.addRow(_("Auto-Fetch Next Sample:"), autoFetchNextSampleCheckBox)
        parent.registerProperty(
            "MONAILabel/autoFetchNextSample",
            ctk.ctkBooleanMapper(autoFetchNextSampleCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        autoUpdateModelCheckBox = qt.QCheckBox()
        autoUpdateModelCheckBox.checked = False
        autoUpdateModelCheckBox.toolTip = _("Enable this option to auto update model after submitting the label")
        groupLayout.addRow(_("Auto-Update Model:"), autoUpdateModelCheckBox)
        parent.registerProperty(
            "MONAILabel/autoUpdateModelV2",
            ctk.ctkBooleanMapper(autoUpdateModelCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        askForUserNameCheckBox = qt.QCheckBox()
        askForUserNameCheckBox.checked = False
        askForUserNameCheckBox.toolTip = _(
            "Enable this option to ask for the user name every time the MONAILabel"
            "extension is loaded for the first time"
        )

        groupLayout.addRow(_("Ask For User Name:"), askForUserNameCheckBox)
        parent.registerProperty(
            "MONAILabel/askForUserName",
            ctk.ctkBooleanMapper(askForUserNameCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        allowOverlapCheckBox = qt.QCheckBox()
        allowOverlapCheckBox.checked = False
        allowOverlapCheckBox.toolTip = _("Enable this option to allow overlapping segmentations")
        groupLayout.addRow(_("Allow Overlapping Segmentations:"), allowOverlapCheckBox)
        parent.registerProperty(
            "MONAILabel/allowOverlappingSegments",
            ctk.ctkBooleanMapper(allowOverlapCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )
        allowOverlapCheckBox.connect("toggled(bool)", self.onUpdateAllowOverlap)

        originalLabelCheckBox = qt.QCheckBox()
        originalLabelCheckBox.checked = True
        originalLabelCheckBox.toolTip = _("Enable this option to first read original label (predictions)")
        groupLayout.addRow(_("Original Labels:"), originalLabelCheckBox)
        parent.registerProperty(
            "MONAILabel/originalLabel",
            ctk.ctkBooleanMapper(originalLabelCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        developerModeCheckBox = qt.QCheckBox()
        developerModeCheckBox.checked = True
        developerModeCheckBox.toolTip = _("Enable this option to find options tab etc...")
        groupLayout.addRow(_("Developer Mode:"), developerModeCheckBox)
        parent.registerProperty(
            "MONAILabel/developerMode",
            ctk.ctkBooleanMapper(developerModeCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        showSegmentsIn3DCheckBox = qt.QCheckBox()
        showSegmentsIn3DCheckBox.checked = False
        showSegmentsIn3DCheckBox.toolTip = _("Enable this option to show segments in 3D (slow) after mask update...")
        groupLayout.addRow(_("Show Segments In 3D:"), showSegmentsIn3DCheckBox)
        parent.registerProperty(
            "MONAILabel/showSegmentsIn3D",
            ctk.ctkBooleanMapper(showSegmentsIn3DCheckBox, "checked", str(qt.SIGNAL("toggled(bool)"))),
            "valueAsInt",
            str(qt.SIGNAL("valueAsIntChanged(int)")),
        )

        vBoxLayout.addWidget(groupBox)
        vBoxLayout.addStretch(1)

    def onUpdateAllowOverlap(self):
        if slicer.util.settingsValue("MONAILabel/allowOverlappingSegments", True, converter=slicer.util.toBool):
            if slicer.util.settingsValue("MONAILabel/fileExtension", None) != ".seg.nrrd":
                slicer.util.warningDisplay(
                    _(
                        "Overlapping segmentations are only available with the '.seg.nrrd' file extension!"
                        "Consider changing MONAILabel file extension."
                    )
                )


class SimplifiedMONAILabelSettingsPanel(ctk.ctkSettingsPanel):
    def __init__(self, *args, **kwargs):
        ctk.ctkSettingsPanel.__init__(self, *args, **kwargs)
        self.ui = _ui_SimplifiedMONAILabelSettingsPanel(self)


class SimplifiedMONAILabelWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation

        self.logic = None
        self._parameterNode = None
        self._volumeNode = None
        self._segmentNode = None
        self._scribblesROINode = None
        self._volumeNodes = []
        self._updatingGUIFromParameterNode = False

        self.info = {}
        self.models = OrderedDict()
        self.trainers = OrderedDict()
        self.config = OrderedDict()
        self.current_sample = None
        self.samples = {}
        self.state = {
            "SegmentationModel": "",
        }
        self.file_ext = ".nii.gz"

        self.dgPositivePointListNode = None
        self.dgPositivePointListNodeObservers = []
        self.dgNegativePointListNode = None
        self.dgNegativePointListNodeObservers = []
        self.ignorePointListNodeAddEvent = False

        self.progressBar = None
        self.tmpdir = None
        self.timer = None

        self.scribblesMode = None
        self.ignoreScribblesLabelChangeEvent = False
        self.deepedit_multi_label = False

        self.optionsSectionIndex = 0
        self.optionsNameIndex = 0

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/SimplifiedMONAILabel.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.NodeAddedEvent, self.onSceneEndImport)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.tmpdir = slicer.util.tempDirectory("slicer-monai-label")
        self.logic = SimplifiedMONAILabelLogic(self.tmpdir, resourcePath=self.resourcePath)

        # Set icons and tune widget properties
        self.ui.serverComboBox.lineEdit().setPlaceholderText("enter server address or leave empty to use default")
        self.ui.fetchServerInfoButton.setIcon(self.icon("refresh-icon.png"))
        self.ui.segmentationButton.setIcon(self.icon("segment.png"))
        self.ui.uploadImageButton.setIcon(self.icon("upload.png"))

        # Connections
        self.ui.fetchServerInfoButton.connect("clicked(bool)", self.onClickFetchInfo)
        self.ui.serverComboBox.connect("currentIndexChanged(int)", self.onClickFetchInfo)
        self.ui.segmentationModelSelector.connect("currentIndexChanged(int)", self.updateParameterNodeFromGUI)
        self.ui.segmentationButton.connect("clicked(bool)", self.onClickSegmentation)
        self.ui.uploadImageButton.connect("clicked(bool)", self.onUploadImage)

        # embedded segment editor
        self.ui.embeddedSegmentEditorWidget.setMRMLScene(slicer.mrmlScene)
        self.ui.embeddedSegmentEditorWidget.setSegmentationNodeSelectorVisible(False)
        self.ui.embeddedSegmentEditorWidget.setSourceVolumeNodeSelectorVisible(False)
        self.ui.embeddedSegmentEditorWidget.setMRMLSegmentEditorNode(self.logic.get_segment_editor_node()) 

        self.initializeParameterNode()
        self.updateServerUrlGUIFromSettings()

        if slicer.util.settingsValue("MONAILabel/askForUserName", False, converter=slicer.util.toBool):
            text = qt.QInputDialog().getText(
                self.parent,
                _("User Name"),
                _("Please enter your name:"),
                qt.QLineEdit.Normal,
                slicer.util.settingsValue("MONAILabel/clientId", None),
            )
            if text:
                settings = qt.QSettings()
                settings.setValue("MONAILabel/clientId", text)

    def cleanup(self):
        self.removeObservers()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def enter(self):
        self.initializeParameterNode()
        if self._segmentNode:
            self.updateGUIFromParameterNode()

    def exit(self):
        self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    def onSceneStartClose(self, caller, event):
        self.state = {
            "SegmentationModel": self.ui.segmentationModelSelector.currentText,
        }

        self._volumeNode = None
        self._segmentNode = None
        self._volumeNodes.clear()
        self.setParameterNode(None)
        self.current_sample = None
        self.samples.clear()
        self._scribblesROINode = None

    def onSceneEndClose(self, caller, event):
        if self.parent.isEntered:
            self.initializeParameterNode()

    def onSceneEndImport(self, caller, event):
        if not self._volumeNode:
            self.updateGUIFromParameterNode()

    def initializeParameterNode(self):
        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.GetNodeReference("InputVolume"):
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

    def setParameterNode(self, inputParameterNode):
        if inputParameterNode:
            self.logic.setDefaultParameters(inputParameterNode)

        if self._parameterNode is not None:
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
        self._parameterNode = inputParameterNode
        if self._parameterNode is not None:
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

        # Initial GUI update
        self.updateGUIFromParameterNode()

    def updateGUIFromParameterNode(self, caller=None, event=None):
        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
        self._updatingGUIFromParameterNode = True

        file_ext = slicer.util.settingsValue("MONAILabel/fileExtension", self.file_ext)
        self.file_ext = file_ext if file_ext else self.file_ext

        # Update node selectors and sliders
        self.ui.inputSelector.clear()
        for v in self._volumeNodes:
            self.ui.inputSelector.addItem(v.GetName())
            self.ui.inputSelector.setToolTip(self.current_sample.get("name", "") if self.current_sample else "")
        if self._volumeNode:
            self.ui.inputSelector.setCurrentIndex(self.ui.inputSelector.findText(self._volumeNode.GetName()))
        self.ui.inputSelector.setEnabled(False)  # Allow only one active scene

        self.ui.uploadImageButton.setEnabled(False)
        if self.info and slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode") and self._volumeNode is None:
            self._volumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            self.initSample({"id": self._volumeNode.GetName(), "session": True}, autosegment=False)
            self.ui.inputSelector.setEnabled(False)

        self.ui.uploadImageButton.setEnabled(self.current_sample and self.current_sample.get("session"))

        self.updateSelector(self.ui.segmentationModelSelector, ["segmentation", "detection"], "SegmentationModel", 0)

        if self.models and [k for k, v in self.models.items() if v["type"] in ("segmentation", "detection")]:
            self.ui.segmentationCollapsibleButton.collapsed = False
            self.ui.segmentationCollapsibleButton.show()
        else:
            self.ui.segmentationCollapsibleButton.hide()

        self.ignoreScribblesLabelChangeEvent = True

        currentLabel = self._parameterNode.GetParameter("CurrentLabel")
        idx = self.ui.labelComboBox.findText(currentLabel) if currentLabel else 0
        idx = 0 if idx < 0 < self.ui.labelComboBox.count else idx

        currentScribbleLabel = self._parameterNode.GetParameter("CurrentScribLabel")
        idx = self.ui.scribLabelComboBox.findText(currentScribbleLabel) if currentScribbleLabel else 0
        idx = 0 if idx < 0 < self.ui.scribLabelComboBox.count else idx
        self.ignoreScribblesLabelChangeEvent = False

        self.ui.appComboBox.clear()
        self.ui.appComboBox.addItem(self.info.get("name", ""))

        datastore_stats = self.info.get("datastore", {})
        current = datastore_stats.get("completed", 0)
        total = datastore_stats.get("total", 0)

        developer_mode = slicer.util.settingsValue("MONAILabel/developerMode", True, converter=slicer.util.toBool)

        self.ui.segmentationButton.setEnabled(
            self.ui.segmentationModelSelector.currentText and self._volumeNode is not None
        )

        # All the GUI updates are done
        self._updatingGUIFromParameterNode = False

    def updateParameterNodeFromGUI(self, caller=None, event=None):
        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

        segmentationModelIndex = self.ui.segmentationModelSelector.currentIndex
        if segmentationModelIndex >= 0:
            segmentationModel = self.ui.segmentationModelSelector.itemText(segmentationModelIndex)
            self._parameterNode.SetParameter("SegmentationModel", segmentationModel)

        self._parameterNode.EndModify(wasModified)

    def updateSelector(self, selector, model_types, param, defaultIndex=0):
        wasSelectorBlocked = selector.blockSignals(True)
        selector.clear()

        for model_name, model in self.models.items():
            if model["type"] in model_types:
                selector.addItem(model_name)
                selector.setItemData(selector.count - 1, model["description"], qt.Qt.ToolTipRole)

        model = self._parameterNode.GetParameter(param)
        model = model if model else self.state.get(param, "")
        modelIndex = selector.findText(model)
        modelIndex = defaultIndex if modelIndex < 0 < selector.count else modelIndex
        selector.setCurrentIndex(modelIndex)

        try:
            modelInfo = self.models[model]
            selector.setToolTip(modelInfo["description"])
        except:
            selector.setToolTip("")
        selector.blockSignals(wasSelectorBlocked)

    def getSelectedOptionSection(self, index=-1):
        logging.info(f"Current Selection Options Section: {INFER}")
        mapping = {"infer": "models"}

        return mapping.get(INFER)

    def getSelectedOptionName(self, index=-1):
        logging.info(f"Current Selection Options Name: INFER")
        return "INFER"

    def getParamsFromConfig(self, section, name):
        self.invalidateConfigTable()

        mapping = {"infer": "models", "train": "trainers", "activelearning": "strategies", "scoring": "scoring"}
        section = mapping.get(section, section)
        sectionConfig = self.info.get(section, {})
        nameConfig = sectionConfig.get(name, {}).get("config", {})

        return {k: v[0] if isinstance(v, list) else v for k, v in nameConfig.items()}

    def invalidateConfigTable(self, selection=-1, name=-1):
        section = self.getSelectedOptionSection(selection)
        name = self.getSelectedOptionName(name)
        if not section or not name:
            return

        mapping = {"infer": "models", "train": "trainers", "activelearning": "strategies", "scoring": "scoring"}
        section = mapping.get(section, section)
        for row in range(self.ui.configTable.rowCount):
            key = str(self.ui.configTable.item(row, 0).text())
            value = self.ui.configTable.item(row, 1)

            v = self.info.get(section, {}).get(name, {}).get("config", {}).get(key, {})
            if value is None:
                value = self.ui.configTable.cellWidget(row, 1)
                if isinstance(value, qt.QCheckBox):
                    value = True if value.checked else False
                else:
                    value = value.currentText
            else:
                value = str(value.text())

            if isinstance(v, bool):
                value = True if value else False
            elif isinstance(v, int):
                value = int(value) if value else 0
            elif isinstance(v, float):
                value = float(value) if value else 0.0
            elif isinstance(v, list):
                v.remove(value)
                v.insert(0, value)
                value = v

            logging.info(f"Invalidate:: {section} => {name} => {key} => {value} => {type(v)}")
            self.info.get(section, {}).get(name, {}).get("config", {})[key] = value

    def currentSegment(self):
        segmentation = self._segmentNode.GetSegmentation()
        segmentId = segmentation.GetSegmentIdBySegmentName(self.ui.labelComboBox.currentText)
        segment = segmentation.GetSegment(segmentId)

        logging.debug(f"Current SegmentID: {segmentId}; Segment: {segment}")
        return segmentId, segment

    def icon(self, name="SimplifiedMONAILabel.png"):
        # It should not be necessary to modify this method
        iconPath = os.path.join(os.path.dirname(__file__), "Resources", "Icons", name)
        if os.path.exists(iconPath):
            return qt.QIcon(iconPath)
        return qt.QIcon()

    def updateServerSettings(self):
        self.logic.setServer(self.serverUrl())
        self.logic.setClientId(slicer.util.settingsValue("MONAILabel/clientId", "user-xyz"))
        self.saveServerUrl()

    def serverUrl(self):
        serverUrl = self.ui.serverComboBox.currentText.strip()
        if not serverUrl:
            serverUrl = "http://127.0.0.1:8000"
        return serverUrl.rstrip("/")

    def saveServerUrl(self):
        self.updateParameterNodeFromGUI()

        # Save selected server URL
        settings = qt.QSettings()
        serverUrl = self.ui.serverComboBox.currentText
        settings.setValue("MONAILabel/serverUrl", serverUrl)

        # Save current server URL to the top of history
        serverUrlHistory = settings.value("MONAILabel/serverUrlHistory")
        if serverUrlHistory:
            serverUrlHistory = serverUrlHistory.split(";")
        else:
            serverUrlHistory = []
        try:
            serverUrlHistory.remove(serverUrl)
        except ValueError:
            pass

        serverUrlHistory.insert(0, serverUrl)
        serverUrlHistory = serverUrlHistory[:10]  # keep up to first 10 elements
        settings.setValue("MONAILabel/serverUrlHistory", ";".join(serverUrlHistory))

        self.updateServerUrlGUIFromSettings()

    def onClickFetchInfo(self):
        self.fetchInfo()

    def fetchInfo(self, showInfo=False):
        if not self.logic:
            return

        start = time.time()
        try:
            self.updateServerSettings()
            info = self.logic.info()
            self.info = info
            if self.info.get("config"):
                slicer.util.errorDisplay(
                    _("Please upgrade the monai server to latest version"),
                    detailedText=traceback.format_exc(),
                )
                return
        except BaseException as e:
            msg = f"Message:: {e.msg}" if hasattr(e, "msg") else ""
            slicer.util.errorDisplay(
                _(
                    "Failed to fetch models from remote server. "
                    "Make sure server address is correct and <server_uri>/info/ "
                    "is accessible in browser.\n{message}"
                ).format(message=msg),
                detailedText=traceback.format_exc(),
            )
            return

        self.models.clear()
        self.config = info.get("config", {})

        model_count = {}
        models = info.get("models", {})
        for k, v in models.items():
            model_type = v.get("type", "segmentation")
            model_count[model_type] = model_count.get(model_type, 0) + 1

            logging.debug(f"{k} = {model_type}")
            self.models[k] = v

        self.updateGUIFromParameterNode()

        msg = ""
        msg += "-----------------------------------------------------\t\n"
        msg += "Total Models Available: \t" + str(len(models)) + "\t\n"
        msg += "-----------------------------------------------------\t\n"
        for model_type in model_count.keys():
            msg += model_type.capitalize() + " Models: \t" + str(model_count[model_type]) + "\t\n"
        msg += "-----------------------------------------------------\t\n"

        if showInfo:
            qt.QMessageBox.information(slicer.util.mainWindow(), "MONAI Label", msg)
        logging.info(msg)
        logging.info(f"Time consumed by fetch info: {time.time() - start:3.1f}")

    def reportProgress(self, progressPercentage):
        if not self.progressBar:
            self.progressBar = slicer.util.createProgressDialog(windowTitle=_("Wait..."), maximum=100)
        self.progressBar.show()
        self.progressBar.activateWindow()
        self.progressBar.setValue(progressPercentage)
        slicer.app.processEvents()

    def initSample(self, sample, autosegment=True):
        sample["VolumeNodeName"] = self._volumeNode.GetName()
        self.current_sample = sample
        self.samples[sample["id"]] = sample
        self._volumeNodes.append(self._volumeNode)

        # Create Empty Segments for all labels for this node
        self.createSegmentNode()
        self.ui.embeddedSegmentEditorWidget.setSegmentationNode(self._segmentNode)
        self.ui.embeddedSegmentEditorWidget.setSourceVolumeNode(self._volumeNode)

        # check if user allows overlapping segments
        if slicer.util.settingsValue("MONAILabel/allowOverlappingSegments", False, converter=slicer.util.toBool):
            # set segment editor to allow overlaps
            self.logic.get_segment_editor_node().SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)

        if self.info.get("labels"):
            self.updateSegmentationMask(None, self.info.get("labels"))

        # Check if user wants to run auto-segmentation on new sample
        if autosegment and slicer.util.settingsValue(
            "MONAILabel/autoRunSegmentationOnNextSample", True, converter=slicer.util.toBool
        ):
            for label in self.info.get("labels", []):
                for name, model in self.models.items():
                    if label in model.get("labels", []):
                        qt.QApplication.restoreOverrideCursor()
                        self.ui.segmentationModelSelector.currentText = name
                        self.onClickSegmentation()
                        return

    def getPermissionForImageDataUpload(self):
        return slicer.util.confirmOkCancelDisplay(
            _(
                "Source volume - without any additional patient information -"
                " will be sent to remote data processing server: {server_url}.\n\n"
                "Click 'OK' to proceed with the segmentation.\n"
                "Click 'Cancel' to not upload any data and cancel segmentation.\n"
            ).format(server_url=self.serverUrl()),
            dontShowAgainSettingsKey="MONAILabel/showImageDataSendWarning",
        )

    def onUploadImage(self, init_sample=True, session=False):
        volumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
        image_id = volumeNode.GetName()

        if not self.getPermissionForImageDataUpload():
            return False

        try:
            qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
            in_file = tempfile.NamedTemporaryFile(suffix=self.file_ext, dir=self.tmpdir).name
            self.reportProgress(5)

            start = time.time()
            slicer.util.saveNode(volumeNode, in_file)
            logging.info(f"Saved Input Node into {in_file} in {time.time() - start:3.1f}s")
            self.reportProgress(30)

            if session:
                self.current_sample["session_id"] = self.logic.create_session(in_file)["session_id"]
            else:
                self.logic.upload_image(in_file, image_id)
                self.current_sample["session"] = False
            self.reportProgress(100)

            self._volumeNode = volumeNode
            if init_sample:
                self.initSample({"id": image_id}, autosegment=False)
            qt.QApplication.restoreOverrideCursor()

            self.updateGUIFromParameterNode()
            return True
        except BaseException as e:
            msg = f"Message:: {e.msg}" if hasattr(e, "msg") else ""
            self.reportProgress(100)
            qt.QApplication.restoreOverrideCursor()
            if session:
                slicer.util.errorDisplay(
                    _("Server Error:: Session creation Failed\nPlease upgrade to latest monailabel version (> 0.2.0)"),
                    detailedText=traceback.format_exc(),
                )
                self.current_sample["session"] = None
            else:
                slicer.util.errorDisplay(
                    _("Failed to upload volume to Server.\n{message}").format(message=msg),
                    detailedText=traceback.format_exc(),
                )
            return False

    def getSessionId(self):
        session_id = None
        if self.current_sample.get("session", False):
            session_id = self.current_sample.get("session_id")
            if not session_id or not self.logic.get_session(session_id):
                self.onUploadImage(init_sample=False, session=True)
                session_id = self.current_sample["session_id"]
        return session_id

    def onClickSegmentation(self):
        if not self.current_sample:
            return

        start = time.time()
        result_file = None
        try:
            qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)

            self.updateServerSettings()

            model = self.ui.segmentationModelSelector.currentText
            image_file = self.current_sample["id"]
            params = self.getParamsFromConfig("infer", model)

            result_file, params = self.logic.infer(model, image_file, params, session_id=self.getSessionId())
            print(f"Result Params for Segmentation: {params}")

            labels = (
                params.get("label_names") if params and params.get("label_names") else self.models[model].get("labels")
            )
            if labels and isinstance(labels, dict):
                labels = [k for k, _ in sorted(labels.items(), key=lambda item: item[1])]
            self.updateSegmentationMask(result_file, labels)
        except BaseException as e:
            msg = f"Message:: {e.msg}" if hasattr(e, "msg") else ""
            slicer.util.errorDisplay(
                _("Failed to run inference in MONAI Label Server.\n{message}").format(message=msg),
                detailedText=traceback.format_exc(),
            )
        finally:
            qt.QApplication.restoreOverrideCursor()
            if result_file and os.path.exists(result_file):
                os.unlink(result_file)

        self.updateGUIFromParameterNode()
        logging.info(f"Time consumed by segmentation: {time.time() - start:3.1f}")

    def createSegmentNode(self):
        if self._volumeNode is None:
            return
        if self._segmentNode is None:
            name = "segmentation_" + self._volumeNode.GetName()
            self._segmentNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
            self._segmentNode.SetReferenceImageGeometryParameterFromVolumeNode(self._volumeNode)
            self._segmentNode.SetName(name)

    def getLabelColor(self, name):
        color = GenericAnatomyColors.get(name.lower())
        return [c / 255.0 for c in color] if color else None

    def updateSegmentationMask(self, in_file, labels, sliceIndex=None, freeze=None):
        # TODO:: Add ROI Node (for Bounding Box if provided in the result)
        start = time.time()
        logging.debug(f"Update Segmentation Mask from: {in_file}")
        if in_file and not os.path.exists(in_file):
            return False

        segmentationNode = self._segmentNode
        segmentation = segmentationNode.GetSegmentation()

        if in_file is None:
            for label in labels:
                if not segmentation.GetSegmentIdBySegmentName(label):
                    segmentation.AddEmptySegment(label, label, self.getLabelColor(label))
            return True

        if in_file.endswith(".seg.nrrd") and self.file_ext == ".seg.nrrd":
            source_node = slicer.modules.segmentations.logic().LoadSegmentationFromFile(in_file, False)
            destination_node = segmentationNode
            destination_segmentations = destination_node.GetSegmentation()
            source_segmentations = source_node.GetSegmentation()

            destination_segmentations.DeepCopy(source_segmentations)

            if self._volumeNode:
                destination_node.SetReferenceImageGeometryParameterFromVolumeNode(self._volumeNode)

            slicer.mrmlScene.RemoveNode(source_node)
        elif in_file.endswith(".json"):
            # Add bounding box ROI nodes, load multiple ROI nodes in the same scene.
            logging.info("Update Detection ROI Bounding Box")
            slicer.util.loadMarkups(in_file)
            detectionROIs = slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsROINode")  # Get all ROI node from scene
            numNodes = detectionROIs.GetNumberOfItems()
            for i in range(numNodes):
                ROINode = detectionROIs.GetItemAsObject(i)
                if ROINode.GetName() != "Scribbles ROI":
                    ROINode.SetName(f"Detection ROI - {i}")
                    ROINode.GetDisplayNode().SetInteractionHandleScale(0.7)  # set handle size
        else:
            labels = [label for label in labels if label != "background"]
            logging.info(f"Update Segmentation Mask using Labels: {labels}")

            # segmentId, segment = self.currentSegment()
            labelImage = sitk.ReadImage(in_file)
            labelmapVolumeNode = sitkUtils.PushVolumeToSlicer(labelImage, None, className="vtkMRMLLabelMapVolumeNode")
            logging.info(f"Time consumed by Import LabelMask: {time.time() - start:3.1f}")

            freeze = [freeze] if freeze and isinstance(freeze, str) else freeze
            logging.info(f"Import only Freezed label: {freeze}")

            if sliceIndex is None and not freeze:
                # List of segments to import
                segmentIds = vtk.vtkStringArray()
                for label in labels:
                    segmentIds.InsertNextValue(label)

                # faster import (based on selected segmentIds)
                slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(
                    labelmapVolumeNode, segmentationNode, segmentIds
                )
                slicer.mrmlScene.RemoveNode(labelmapVolumeNode)
            else:
                existingCount = segmentation.GetNumberOfSegments()
                existing_label_ids = {}
                for label in labels:
                    id = segmentation.GetSegmentIdBySegmentName(label)
                    if id:
                        existing_label_ids[label] = id

                # slower import (import all - use only when you have to update one particular slice for 2D)
                slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(
                    labelmapVolumeNode, segmentationNode
                )
                slicer.mrmlScene.RemoveNode(labelmapVolumeNode)

                addedCount = segmentation.GetNumberOfSegments() - existingCount
                addedSegmentIds = [segmentation.GetNthSegmentID(existingCount + i) for i in range(addedCount)]

                self.ui.embeddedSegmentEditorWidget.setSegmentationNode(segmentationNode)
                self.ui.embeddedSegmentEditorWidget.setSourceVolumeNode(self._volumeNode)

                for i, segmentId in enumerate(addedSegmentIds):
                    label = labels[i] if i < len(labels) else f"unknown {i}"
                    if freeze and label not in freeze:
                        logging.info(f"Discard label update for: {label}")
                    else:
                        segment = segmentation.GetSegment(segmentId)
                        logging.info(f"select segmentation with id: {segmentId} => {segment.GetName()} => {label}")
                        if label in existing_label_ids:
                            l_start = time.time()
                            label_id = existing_label_ids[label]

                            self.ui.embeddedSegmentEditorWidget.setCurrentSegmentID(label_id)
                            effect = self.ui.embeddedSegmentEditorWidget.effectByName("Logical operators")

                            if sliceIndex is not None:
                                selectedSegmentLabelmap = effect.selectedSegmentLabelmap()
                                dims = selectedSegmentLabelmap.GetDimensions()
                                for x in range(dims[0]):
                                    for y in range(dims[1]):
                                        selectedSegmentLabelmap.SetScalarComponentFromDouble(x, y, sliceIndex, 0, 0)

                                logging.info(f"{label} - Time to Clean the slice: {time.time() - l_start:3.1f}")

                            l_start = time.time()
                            newLabelmap = slicer.vtkOrientedImageData()
                            segmentationNode.GetBinaryLabelmapRepresentation(segmentId, newLabelmap)
                            op = (
                                slicer.qSlicerSegmentEditorAbstractEffect.ModificationModeSet
                                if sliceIndex is None
                                else slicer.qSlicerSegmentEditorAbstractEffect.ModificationModeAdd
                            )
                            effect.modifySelectedSegmentByLabelmap(newLabelmap, op)
                            logging.info(f"{label} - Time to Update the segment: {time.time() - l_start:3.1f}")

                    segmentationNode.RemoveSegment(segmentId)
                    logging.info(f"Time consumed until Import Segment => {label}: {time.time() - start:3.1f}")

        if slicer.util.settingsValue("MONAILabel/showSegmentsIn3D", False, converter=slicer.util.toBool):
            self.showSegmentationsIn3D()

        logging.info(f"Time consumed by updateSegmentationMask: {time.time() - start:3.1f}")
        return True

    def showSegmentationsIn3D(self):
        # add closed surface representation
        if self._segmentNode:
            self._segmentNode.CreateClosedSurfaceRepresentation()
        view = slicer.app.layoutManager().threeDWidget(0).threeDView()
        view.resetFocalPoint()

    def updateServerUrlGUIFromSettings(self):
        # Save current server URL to the top of history
        settings = qt.QSettings()
        serverUrlHistory = settings.value("MONAILabel/serverUrlHistory")

        wasBlocked = self.ui.serverComboBox.blockSignals(True)
        self.ui.serverComboBox.clear()
        if serverUrlHistory:
            self.ui.serverComboBox.addItems(serverUrlHistory.split(";"))
        self.ui.serverComboBox.setCurrentText(settings.value("MONAILabel/serverUrl"))
        self.ui.serverComboBox.blockSignals(wasBlocked)

class SimplifiedMONAILabelLogic(ScriptedLoadableModuleLogic):
    def __init__(self, tmpdir=None, server_url=None, progress_callback=None, client_id=None, resourcePath=None):
        ScriptedLoadableModuleLogic.__init__(self)

        self.server_url = server_url
        self.tmpdir = slicer.util.tempDirectory("slicer-monai-label") if tmpdir is None else tmpdir
        self.client_id = client_id
        self.resourcePath = resourcePath
        self.username = None
        self.password = None
        self.auth_token = None

        self.volumeToSessions = dict()
        self.progress_callback = progress_callback

    def setDefaultParameters(self, parameterNode):
        if not parameterNode.GetParameter("SegmentationModel"):
            parameterNode.SetParameter("SegmentationModel", "")
        if not parameterNode.GetParameter("DeepgrowModel"):
            parameterNode.SetParameter("DeepgrowModel", "")
        if not parameterNode.GetParameter("ScribblesMethod"):
            parameterNode.SetParameter("ScribblesMethod", "")

    def __del__(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def setServer(self, server_url=None):
        if self.server_url != server_url:
            self.username = None
            self.password = None
            self.auth_token = None

        self.server_url = server_url if server_url else "http://127.0.0.1:8000"

    def setClientId(self, client_id):
        self.client_id = client_id if client_id else "user-xyz"

    def setProgressCallback(self, progress_callback=None):
        self.progress_callback = progress_callback

    def reportProgress(self, progress):
        if self.progress_callback:
            self.progress_callback(progress)

    def get_segment_editor_node(self):
        # Use the Segment Editor module's parameter node for the embedded segment editor widget.
        # This ensures that if the user switches to the Segment Editor then the selected
        # segmentation node, volume node, etc. are the same.
        segmentEditorSingletonTag = "SegmentEditor"
        segmentEditorNode = slicer.mrmlScene.GetSingletonNode(segmentEditorSingletonTag, "vtkMRMLSegmentEditorNode")
        if segmentEditorNode is None:
            segmentEditorNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLSegmentEditorNode")
            segmentEditorNode.UnRegister(None)
            segmentEditorNode.SetSingletonTag(segmentEditorSingletonTag)
            segmentEditorNode = slicer.mrmlScene.AddNode(segmentEditorNode)
        return segmentEditorNode

    def _client(self):
        mc = MONAILabelClient(self.server_url, self.tmpdir, self.client_id)
        if mc.auth_enabled():
            if not self.username or not self.password:
                dlg = LoginDialog(username=self.client_id, password="", resourcePath=self.resourcePath)
                dlg.exec()

                self.username = dlg.ui.username.text
                self.password = dlg.ui.password.text

            if self.auth_token:
                mc.update_auth(self.auth_token)

            # TODO:: JWT token can be validated (with additional py dependencies) to avoid further calls to server
            if not self.auth_token or not mc.auth_valid_token():
                try:
                    print(f"Fetching new Token for: {self.username}")
                    self.auth_token = mc.auth_token(self.username, self.password)
                    mc.update_auth(self.auth_token)
                except:
                    self.username = None
                    self.password = None
                    self.auth_token = None
        return mc

    def info(self):
        return self._client().info()

    def datastore(self):
        return self._client().datastore()

    def download_label(self, label_id, tag):
        return self._client().download_label(label_id, tag)

    def next_sample(self, strategy, params={}):
        return self._client().next_sample(strategy, params)

    def create_session(self, image_in):
        return self._client().create_session(image_in)

    def get_session(self, session_id):
        return self._client().get_session(session_id)

    def remove_session(self, session_id):
        return self._client().remove_session(session_id)

    def upload_image(self, image_in, image_id=None):
        return self._client().upload_image(image_in, image_id)

    def save_label(self, image_in, label_in, params):
        return self._client().save_label(image_in, label_in, params=params)

    def infer(self, model, image_in, params={}, label_in=None, file=None, session_id=None):
        logging.debug("Preparing input data for segmentation")
        self.reportProgress(0)

        client = self._client()
        params["result_extension"] = ".nrrd"  # expect .nrrd
        params["result_dtype"] = "uint8"
        result_file, params = client.infer(model, image_in, params, label_in, file, session_id)

        logging.debug(f"Image Response: {result_file}")
        logging.debug(f"JSON  Response: {params}")

        self.reportProgress(100)
        return result_file, params

    def train_start(self, model=None, params={}):
        return self._client().train_start(model, params)

    def train_status(self, check_if_running):
        return self._client().train_status(check_if_running)

    def train_stop(self):
        return self._client().train_stop()


class LoginDialog(qt.QDialog):
    def __init__(self, username, password, resourcePath):
        super().__init__()
        self.setWindowTitle(_("User Login"))

        layout = qt.QVBoxLayout()
        uiWidget = slicer.util.loadUI(resourcePath("UI/LoginDialog.ui"))
        layout.addWidget(uiWidget)

        self.ui = slicer.util.childWidgetVariables(uiWidget)
        self.setLayout(layout)
        self.ui.username.setText(username)
        self.ui.password.setText(password if password else "")
        self.ui.loginButton.connect("clicked(bool)", self.onLogin)

    def onLogin(self):
        self.close()


class SimplifiedMONAILabelTest(ScriptedLoadableModuleTest):
    def setUp(self):
        slicer.mrmlScene.Clear()

    def runTest(self):
        self.setUp()
        self.test_MONAILabel1()

    def test_MONAILabel1(self):
        self.delayDisplay("Test passed")


INFER = "INFER"
TRAIN = "TRAIN"
ACTIVELEARNING = "ACTIVELEARNING"
SCORING = "SCORING"
