# settings.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from gui.settingsDialogs import SettingsPanel
from gui import guiHelper
import wx
from logHandler import log
from . import addonConfig


class QuickNotetakerPanel(SettingsPanel):
	# Translators: the title of the Quick Notetaker panel in NVDA's settings
	title = _("Quick Notetaker")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: the label of the control in Quick Notetaker settings panel for choosing a folder where notes data will be stored
		notesDataGroupText = _("&Notes data directory:")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=notesDataGroupText)
		groupHelper = sHelper.addItem(guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		groupBox = groupSizer.GetStaticBox()
		# Translators: the label of a button to browse for a directory
		browseText = _("Browse...")
		notesDataDirDialogTitle = _(
			# Translators: The title of the dialog presented when browsing for the directory where quick notetaker notes data will be stored
			"Select a directory where the notes data of Quick Notetaker will be stored"
		)
		notesDataPathHelper = guiHelper.PathSelectionHelper(groupBox, browseText, notesDataDirDialogTitle)
		notesDataEntryControl = groupHelper.addItem(notesDataPathHelper)
		self.notesDataDirectoryEdit = notesDataEntryControl.pathControl
		self.notesDataDirectoryEdit.Value = addonConfig.getValue("notesDataPath")
		# Translators: the label of the control in Quick Notetaker settings panel for choosing a default folder where the add-on documents will be saved
		directoryGroupText = _("&Default documents directory:")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=directoryGroupText)
		groupHelper = sHelper.addItem(guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		groupBox = groupSizer.GetStaticBox()
		# Translators: the label of a button to browse for a directory
		browseText = _("Browse...")
		dirDialogTitle = _(
			# Translators: The title of the dialog presented when browsing for the directory where quick notetaker documents will be stored
			"Select a default directory where the documents of Quick Notetaker will be stored"
		)
		directoryPathHelper = guiHelper.PathSelectionHelper(groupBox, browseText, dirDialogTitle)
		directoryEntryControl = groupHelper.addItem(directoryPathHelper)
		self.documentDirectoryEdit = directoryEntryControl.pathControl
		self.documentDirectoryEdit.Value = addonConfig.getValue("notesDocumentsPath")
		askWhereToSaveDocxText = _(
			# Translators: the label of a check box in Quick Notetaker settings panel
			"Ask me each time &where to save the note's corresponding Microsoft Word document"
		)
		self.askWhereToSaveDocxCheckbox = sHelper.addItem(wx.CheckBox(self, label=askWhereToSaveDocxText))
		self.askWhereToSaveDocxCheckbox.Value = addonConfig.getValue("askWhereToSaveDocx")
		openFileAfterCreationText = _(
			# Translators: the label of a check box in Quick Notetaker settings panel
			"&Open the note's corresponding Microsoft Word document after saving or updating"
		)
		self.openAfterCreationCheckbox = sHelper.addItem(wx.CheckBox(self, label=openFileAfterCreationText))
		self.openAfterCreationCheckbox.Value = addonConfig.getValue("openFileAfterCreation")
		captureActiveWindowTitleText = _(
			# Translators: the label of a check box in Quick Notetaker settings panel
			"&Capture the active window title when creating a new note"
		)
		self.captureActiveWindowTitleCheckbox = sHelper.addItem(
			wx.CheckBox(self, label=captureActiveWindowTitleText)
		)
		self.captureActiveWindowTitleCheckbox.Value = addonConfig.getValue("captureActiveWindowTitle")
		rememberTakerSizeAndPosText = _(
			# Translators: the label of a check box in Quick Notetaker settings panel
			"&Remember the note taker window size and position"
		)
		self.rememberTakerSizeAndPosCheckbox = sHelper.addItem(
			wx.CheckBox(self, label=rememberTakerSizeAndPosText)
		)
		self.rememberTakerSizeAndPosCheckbox.Value = addonConfig.getValue("rememberTakerSizeAndPos")
		autoAlignTextText = _(
			# Translators: the label of a check box in Quick Notetaker settings panel
			"Au&to align text when editing notes (relevant for RTL languages)"
		)
		self.autoAlignTextCheckbox = sHelper.addItem(wx.CheckBox(self, label=autoAlignTextText))
		self.autoAlignTextCheckbox.Value = addonConfig.getValue("autoAlignText")

	def onSave(self):
		log.debug("Saving Quick Notetaker settings")
		oldNotesDataPath = addonConfig.getValue("notesDataPath")
		newNotesDataPath = os.path.normpath(self.notesDataDirectoryEdit.Value)

		# Validate path is not empty
		if not newNotesDataPath or not newNotesDataPath.strip():
			log.error("Notes data path cannot be empty")
			wx.MessageBox(
				_("Please specify a directory for notes data storage."),
				_("Invalid Path"),
				wx.ICON_ERROR,
			)
			return

		log.debug(f"Old notes data path: {oldNotesDataPath}")
		log.debug(f"New notes data path: {newNotesDataPath}")

		# Migrate notes data if the path changed
		if oldNotesDataPath != newNotesDataPath:
			log.info("Notes data path changed, attempting migration")
			wasSuccessful = self._migrateNotesData(oldNotesDataPath, newNotesDataPath)
			if not wasSuccessful:
				# Migration failed, don't save the new path
				log.error("Migration failed, settings not saved")
				return

		addonConfig.setValue("notesDataPath", newNotesDataPath)
		log.info(f"Updated notes data path to: {newNotesDataPath}")
		addonConfig.setValue("notesDocumentsPath", os.path.normpath(self.documentDirectoryEdit.Value))
		addonConfig.setValue("askWhereToSaveDocx", self.askWhereToSaveDocxCheckbox.Value)
		addonConfig.setValue("openFileAfterCreation", self.openAfterCreationCheckbox.Value)
		addonConfig.setValue("captureActiveWindowTitle", self.captureActiveWindowTitleCheckbox.Value)
		addonConfig.setValue("rememberTakerSizeAndPos", self.rememberTakerSizeAndPosCheckbox.Value)
		addonConfig.setValue("autoAlignText", self.autoAlignTextCheckbox.Value)
		log.debug("Quick Notetaker settings saved successfully")

	def _migrateNotesData(self, oldPath, newPath):
		"""Migrate notes data from old directory to new directory.

		Returns:
			True if migration was successful or not needed
			False if migration failed
		"""
		import shutil

		log.info(f"Starting notes data migration from {oldPath} to {newPath}")
		try:
			if not os.path.isdir(oldPath):
				log.debug(f"Old path does not exist: {oldPath}, skipping migration")
				return True  # Nothing to migrate

			# Check if old file exists
			oldNotesFile = os.path.join(oldPath, "notes.json")
			if not os.path.isfile(oldNotesFile):
				log.debug(f"No notes.json found in {oldPath}, skipping migration")
				return True  # No file to migrate

			log.debug(f"Found notes file at {oldNotesFile}")

			# Create new directory if it doesn't exist
			if not os.path.isdir(newPath):
				log.info(f"Creating new data directory: {newPath}")
				os.makedirs(newPath, exist_ok=True)

			# Check if file already exists at destination
			newNotesFile = os.path.join(newPath, "notes.json")
			if os.path.isfile(newNotesFile):
				log.warning(f"Notes file already exists at destination: {newNotesFile}")
				dlg = wx.MessageDialog(
					None,
					_(
						"Notes already exist at the destination. Do you want to keep the existing notes at the new location?"
					),
					_("Notes Already Exist"),
					wx.YES_NO | wx.ICON_QUESTION,
				)
				result = dlg.ShowModal()
				dlg.Destroy()
				if result == wx.ID_YES:
					log.info("User chose to keep existing notes at destination, skipping migration")
					wx.MessageBox(
						_("Existing notes at destination will be kept."),
						_("Migration Skipped"),
						wx.ICON_INFORMATION,
					)
					return True  # Accept existing file, don't migrate
				else:
					log.info("User declined to keep existing notes")
					return False  # User cancelled migration

			# Copy notes.json file
			log.info(f"Copying notes file from {oldNotesFile} to {newNotesFile}")
			shutil.copy2(oldNotesFile, newNotesFile)
			log.info(f"Successfully migrated notes data from {oldPath} to {newPath}")
			wx.MessageBox(
				_(f"Notes successfully migrated to {newPath}"),
				_("Migration Complete"),
				wx.ICON_INFORMATION,
			)
			return True
		except (IOError, OSError) as e:
			log.exception(f"I/O error during migration: {e}")
			msg = _(f"Failed to migrate notes data: {e}")
			log.error(msg)
			wx.MessageBox(msg, _("Migration Error"), wx.ICON_ERROR)
			return False
		except Exception as e:
			log.exception(f"Unexpected error during migration: {e}")
			wx.MessageBox(
				_("An unexpected error occurred during migration. Check the NVDA log for details."),
				_("Migration Error"),
				wx.ICON_ERROR,
			)
			return False
