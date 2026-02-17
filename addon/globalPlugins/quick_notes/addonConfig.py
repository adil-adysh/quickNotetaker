# addonConfig.py
# -*- coding: utf-8 -*-
# A part from Quick Notes add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import os
from logHandler import log


def initialize():
	"""Initialize configuration spec for quick_notes add-on at runtime.

	This runs when the addon is loaded (in GlobalPlugin.__init__).
	Registers the complete spec and ensures config section exists.
	This is the only place where the config spec is registered.
	"""
	configSpec = {
		# Data storage paths
		"notesDataPath": f"string(default={os.path.normpath(os.path.join(os.path.expanduser('~'), 'appdata', 'roaming', 'nvda', 'quick_notes data')) if os.name == 'nt' else os.path.normpath(os.path.join(os.path.expanduser('~'), '.config', 'nvda', 'quick_notes data'))})",
		"notesDocumentsPath": f"string(default={os.path.normpath(os.path.expanduser('~/documents/quick_notes'))})",
		# User preferences
		"askWhereToSaveDocx": "boolean(default=False)",
		"openFileAfterCreation": "boolean(default=False)",
		"captureActiveWindowTitle": "boolean(default=True)",
		"rememberNotesWindowSizeAndPos": "boolean(default=False)",
		"autoAlignText": "boolean(default=True)",
		# Pandoc settings
		"pandocUserPath": "string(default='')",
		"showPandocPromptOnInstall": "boolean(default=True)",
		# Window position and size
		"notesXPos": "integer(default=-1)",
		"notesYPos": "integer(default=-1)",
		"notesWidth": "integer(default=500, min=200, max=2000)",
		"notesHeight": "integer(default=500, min=200, max=2000)",
	}

	# Register spec using setdefault + update pattern
	# This ensures the spec exists and is properly merged
	config.conf.spec.setdefault("quick_notes", {})
	config.conf.spec["quick_notes"].update(configSpec)

	# Ensure the quick_notes section exists in config data
	if "quick_notes" not in config.conf:
		config.conf["quick_notes"] = {}


def getValue(key):
	"""Get a configuration value safely.

	Args:
		key: The configuration key to retrieve

	Returns:
		The configuration value, or None if not found
	"""
	try:
		return config.conf["quick_notes"][key]
	except KeyError:
		# Config key doesn't exist, likely upgrading from older version
		# Re-initialize config to ensure all defaults are set
		log.warning(f"Config key '{key}' not found, reinitializing config spec")
		initialize()
		try:
			return config.conf["quick_notes"][key]
		except KeyError:
			log.error(f"Config key '{key}' still missing after reinitialization")
			return None
	except Exception as e:
		log.exception(f"Error retrieving config key '{key}': {e}")
		return None


def setValue(key, value):
	"""Set a configuration value and persist it.

	Args:
		key: The configuration key to set
		value: The value to set
	"""
	try:
		config.conf["quick_notes"][key] = value
		# Ensure the configuration is saved to disk
		if hasattr(config.conf, "save"):
			config.conf.save()
	except Exception as e:
		log.exception(f"Error setting config key '{key}' to value '{value}': {e}")
