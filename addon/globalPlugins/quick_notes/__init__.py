# __init__.py
# -*- coding: utf-8 -*-
# A part from Quick Notes add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
from scriptHandler import script
import gui
from . import dialogs
from .dialogs import NoteTakerDialog, NotesManagerDialog
from .settingsPanel import QuickNotesPanel
from . import notesManager
import os
from .constants import TEMP_FILES_PATH
from . import addonConfig
import api
import addonHandler
import textInfos
import ui


addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		addonConfig.initialize()
		notesManager.initialize()
		documentsPath = addonConfig.getValue("notesDocumentsPath")
		try:
			os.mkdir(documentsPath)
		except FileNotFoundError:
			# The user has no documents directory
			# Create the add-on documents folder in the user root folder instead
			documentsPath = os.path.normpath(os.path.join(os.path.expanduser("~"), "quick_notes"))
			addonConfig.setValue("notesDocumentsPath", documentsPath)
			os.mkdir(documentsPath)
		except FileExistsError:
			pass
		try:
			os.mkdir(TEMP_FILES_PATH)
		except FileExistsError:
			pass
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(QuickNotesPanel)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(QuickNotesPanel)
		if not os.path.isdir(TEMP_FILES_PATH):
			return
		for file in os.listdir(TEMP_FILES_PATH):
			os.remove(os.path.join(TEMP_FILES_PATH, file))

	# Translators: the name of the add-on category in input gestures
	scriptCategory = _("Quick Notes")

	@script(
		# Translators: the description for the command to open the notetaker dialog
		description=_("Shows the Notetaker interface for writing a new note"),
		gesture="kb:NVDA+alt+n",
	)
	def script_showNoteTakerUI(self, gesture):
		noteTitle = None
		if addonConfig.getValue("captureActiveWindowTitle"):
			noteTitle = api.getForegroundObject().name
		gui.mainFrame.prePopup()
		dialogs.noteTakerInstance = NoteTakerDialog(noteTitle=noteTitle)
		dialogs.noteTakerInstance.Show()
		gui.mainFrame.postPopup()

	@script(
		description=_(
			# Translators: the description for the command to create a note from selected text
			"Creates a new note with the currently selected text in browse mode"
		),
		gesture="kb:NVDA+shift+alt+s",
	)
	def script_createNoteFromSelection(self, gesture):
		selectedText = self._getSelectedText()
		if not selectedText:
			ui.message(
				# Translators: Message when no text is selected
				_("No text is selected. Please select some text and try again.")
			)
			return
		noteTitle = None
		if addonConfig.getValue("captureActiveWindowTitle"):
			noteTitle = api.getForegroundObject().name
		gui.mainFrame.prePopup()
		dialogs.noteTakerInstance = NoteTakerDialog(noteTitle=noteTitle, noteContent=selectedText)
		dialogs.noteTakerInstance.Show()
		gui.mainFrame.postPopup()

	def _getSelectedText(self):
		"""Get selected text from virtual buffer (browse mode) or active control.

		Returns:
			str: The selected text, or None if no selection exists.
		"""
		try:
			obj = api.getFocusObject()
			# For virtual buffer (browse mode), try the tree interceptor first
			ti = getattr(obj, "treeInterceptor", None)
			if ti:
				try:
					info = ti.makeTextInfo(textInfos.POSITION_SELECTION)
					if not info.isCollapsed:
						return info.text
				except (RuntimeError, NotImplementedError, AttributeError, TypeError):
					pass

			# Fall back to the focused object itself
			try:
				info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
				if not info.isCollapsed:
					return info.text
			except (RuntimeError, NotImplementedError, AttributeError, TypeError):
				pass

			return None
		except Exception as e:
			# Log any unexpected errors
			import logging

			logging.debug(f"Error getting selected text: {e}")
			return None

	@script(
		description=_(
			# Translators: the description for the command to open the Notes Manager
			"Shows the Notes Manager interface for viewing and managing notes"
		),
		gesture="kb:NVDA+alt+v",
	)
	def script_showNotesManagerDialogUI(self, gesture):
		gui.mainFrame.prePopup()
		dialogs.notesManagerInstance = NotesManagerDialog()
		dialogs.notesManagerInstance.Show()
		gui.mainFrame.postPopup()
