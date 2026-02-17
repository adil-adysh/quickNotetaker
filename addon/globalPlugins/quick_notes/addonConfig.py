# addonConfig.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import os
import wx


def initialize():
	configSpec = {
		"notesDataPath": f"string(default={os.path.normpath(os.path.join(os.path.expanduser('~'), 'appdata', 'roaming', 'nvda', 'quick_notes data')) if os.name == 'nt' else os.path.normpath(os.path.join(os.path.expanduser('~'), '.config', 'nvda', 'quick_notes data'))})",
		"notesDocumentsPath": f"string(default={os.path.normpath(os.path.expanduser('~/documents/quick_notes'))})",
		"askWhereToSaveDocx": "boolean(default=False)",
		"openFileAfterCreation": "boolean(default=False)",
		"captureActiveWindowTitle": "boolean(default=True)",
		"rememberTakerSizeAndPos": "boolean(default=False)",
		"autoAlignText": "boolean(default=true)",
		"pandocUserPath": "string(default='')",
		"takerXPos": f"integer(default={wx.DefaultPosition.x})",
		"takerYPos": f"integer(default={wx.DefaultPosition.y})",
		"takerWidth": "integer(default=500)",
		"takerHeight": "integer(default=500)",
	}
	config.conf.spec["quick_notes"] = configSpec


def getValue(key):
	try:
		return config.conf["quick_notes"][key]
	except KeyError:
		# Config key doesn't exist, likely upgrading from older version
		# Re-initialize config to ensure all defaults are set
		initialize()
		return config.conf["quick_notes"][key]


def setValue(key, value):
	config.conf["quick_notes"][key] = value
