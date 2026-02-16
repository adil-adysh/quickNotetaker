# -*- coding: UTF-8 -*-
"""
NVDA Add-on: quickNotetaker
installTasks to check for Pandoc in system path and guide the user to download if not found.
"""

import addonHandler
import config
import logging
import os
import shutil
import gettext

_ = gettext.gettext

addonHandler.initTranslation()

confspec = {
	"pandocUserPath": "string(default='')",
	"showPandocPromptOnInstall": "boolean(default=True)",
}
config.conf.spec.setdefault("quickNotetaker", {})
config.conf.spec["quickNotetaker"].update(confspec)

logger = logging.getLogger("quickNotetaker.installTasks")

PANDOC_RELEASE_URL = "https://github.com/jgm/pandoc/releases/latest"

user_pandoc_path = config.conf["quickNotetaker"].get("pandocUserPath", "")


# Helper to locate pandoc
def locate_pandoc(user_path=None):
	pandoc_bin_name = "pandoc.exe" if os.name == "nt" else "pandoc"
	# 1. User-specified path
	if user_path and os.path.isfile(user_path):
		logger.info(f"Using user-specified Pandoc path: {user_path}")
		return user_path
	# 2. Add-on lib path
	base_path = os.path.dirname(__file__)
	lib_dir = os.path.join(base_path, "lib")
	pandoc_dir = os.path.join(lib_dir, "pandoc")
	pandoc_bin = os.path.join(pandoc_dir, pandoc_bin_name)
	if os.path.isfile(pandoc_bin):
		logger.info(f"Found Pandoc in add-on lib: {pandoc_bin}")
		return pandoc_bin
	# 3. System PATH
	system_pandoc = shutil.which(pandoc_bin_name)
	if system_pandoc:
		logger.info(f"Found Pandoc in system PATH: {system_pandoc}")
		return system_pandoc
	logger.warning("Pandoc not found in user path, add-on lib, or system PATH.")
	return None


def onInstall():
	if not config.conf["quickNotetaker"].get("showPandocPromptOnInstall", True):
		return
	pandoc_path = locate_pandoc(user_pandoc_path)
	if pandoc_path:
		logger.info(f"Pandoc detected at {pandoc_path}.")
		return
	# Only import gui.message when needed, avoid shadowing
	try:
		from gui.message import MessageDialog, ReturnCode
	except ImportError:
		logger.error("Could not import gui.message. Pandoc prompt will not be shown.")
		return
	result = MessageDialog.ask(
		_(
			"Pandoc is required for QuickNotetaker to convert documents. Would you like to open the Pandoc releases page to download it?"
		),
		_("Pandoc Not Found"),
	)
	if result == getattr(ReturnCode, "YES", 1):
		import webbrowser

		webbrowser.open(PANDOC_RELEASE_URL)
