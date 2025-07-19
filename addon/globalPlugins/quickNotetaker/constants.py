# constants.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalVars
import os
import sys
import shutil
import config

CONFIG_PATH = globalVars.appArgs.configPath

QUICK_NOTETAKER_PATH = os.path.join(CONFIG_PATH, "addons", "quickNotetaker", "globalPlugins")

QUICK_NOTETAKER_PATH_DEV = os.path.join(CONFIG_PATH, "scratchpad", "globalPlugins", "quickNotetaker")

# Remember to comment out in production
# QUICK_NOTETAKER_PATH = QUICK_NOTETAKER_PATH_DEV

DATA_DIR_PATH = os.path.join(CONFIG_PATH, "Quick Notetaker data")

DATA_FILE_PATH = os.path.join(DATA_DIR_PATH, "notes.json")

# Define configuration spec for quickNotetaker
confspec = {
	"pandocUserPath": "string(default='')",
	# ...other config entries...
}
config.conf.spec.setdefault("quickNotetaker", {})
config.conf.spec["quickNotetaker"].update(confspec)

# Use config for user Pandoc path
user_pandoc_path = config.conf["quickNotetaker"].get("pandocUserPath", "")


def get_pandoc_path(base_path, user_path=None):
	"""
	Returns the full path to the pandoc executable.
	Priority:
	1. If user_path is provided and valid, use it.
	2. Use the pandoc binary in the 'pandoc' folder inside 'lib'.
	3. If not found, look for pandoc in the system PATH.
	Returns the full path to the pandoc executable, or None if not found.
	"""
	pandoc_bin_name = "pandoc.exe" if os.name == "nt" else "pandoc"
	# 1. User-specified path
	if user_path and os.path.isfile(user_path):
		return user_path
	# 2. Add-on lib path
	lib_dir = os.path.join(base_path, "quickNotetaker", "lib")
	pandoc_dir = os.path.join(lib_dir, "pandoc")
	pandoc_bin = os.path.join(pandoc_dir, pandoc_bin_name)
	if os.path.isfile(pandoc_bin):
		return pandoc_bin
	# 3. System PATH
	system_pandoc = shutil.which(pandoc_bin_name)
	if system_pandoc:
		return system_pandoc
	return None


PANDOC_PATH = get_pandoc_path(QUICK_NOTETAKER_PATH, user_pandoc_path)
PANDOC_PATH_DEV = get_pandoc_path(QUICK_NOTETAKER_PATH_DEV, user_pandoc_path)
# Remember to comment out in production
# PANDOC_PATH = PANDOC_PATH_DEV

TEMP_FILES_PATH = os.path.join(QUICK_NOTETAKER_PATH, "tempFiles")

DEFAULT_DOCUMENTS_PATH = os.path.normpath(os.path.expanduser("~/documents/quickNotetaker"))
