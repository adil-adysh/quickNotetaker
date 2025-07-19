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

CONFIG_PATH = globalVars.appArgs.configPath

QUICK_NOTETAKER_PATH = os.path.join(
    CONFIG_PATH, "addons", "quickNotetaker", "globalPlugins")

QUICK_NOTETAKER_PATH_DEV = os.path.join(
    CONFIG_PATH, "scratchpad", "globalPlugins", "quickNotetaker")

# Remember to comment out in production
# QUICK_NOTETAKER_PATH = QUICK_NOTETAKER_PATH_DEV

DATA_DIR_PATH = os.path.join(CONFIG_PATH, "Quick Notetaker data")

DATA_FILE_PATH = os.path.join(DATA_DIR_PATH, "notes.json")

# User can specify a custom Pandoc path here (or via config in future)
USER_PANDOC_PATH = None  # Set to a string path if user wants to override

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

PANDOC_PATH = get_pandoc_path(QUICK_NOTETAKER_PATH, USER_PANDOC_PATH)
PANDOC_PATH_DEV = get_pandoc_path(QUICK_NOTETAKER_PATH_DEV, USER_PANDOC_PATH)
# Remember to comment out in production
# PANDOC_PATH = PANDOC_PATH_DEV

TEMP_FILES_PATH = os.path.join(QUICK_NOTETAKER_PATH, "tempFiles")

DEFAULT_DOCUMENTS_PATH = os.path.normpath(
    os.path.expanduser("~/documents/quickNotetaker"))
