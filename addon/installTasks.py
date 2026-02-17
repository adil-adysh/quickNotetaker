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
	"notesDocumentsPath": f"string(default={os.path.normpath(os.path.expanduser('~/documents/quick_notes'))})",
	"askWhereToSaveDocx": "boolean(default=False)",
	"openFileAfterCreation": "boolean(default=False)",
	"captureActiveWindowTitle": "boolean(default=True)",
	"rememberTakerSizeAndPos": "boolean(default=False)",
	"autoAlignText": "boolean(default=True)",
	"takerXPos": "integer(default=-1)",
	"takerYPos": "integer(default=-1)",
	"takerWidth": "integer(default=500)",
	"takerHeight": "integer(default=500)",
}
config.conf.spec.setdefault("quick_notes", {})
config.conf.spec["quick_notes"].update(confspec)

logger = logging.getLogger("quick_notes.installTasks")

PANDOC_RELEASE_URL = "https://github.com/jgm/pandoc/releases/latest"

user_pandoc_path = config.conf["quick_notes"].get("pandocUserPath", "")


# Helper to locate pandoc
def locate_pandoc(user_path=None):
	pandoc_bin_name = "pandoc.exe" if os.name == "nt" else "pandoc"
	# 1. User-specified path
	if user_path and os.path.isfile(user_path):
		logger.info(f"Using user-specified Pandoc path: {user_path}")
		return user_path
	# 2. Add-on lib path
	base_path = os.path.dirname(__file__)
	lib_dir = os.path.join(base_path, "globalPlugins", "quick_notes", "lib")
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
	if not config.conf["quick_notes"].get("showPandocPromptOnInstall", True):
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


def onUninstall():
	"""Clean up addon configuration when the addon is uninstalled.

	NVDA calls this function during startup after the user has chosen to remove the add-on.
	This removes the addon's config section while preserving user data (notes.json).

	Note: This function runs before other NVDA components are initialized,
	so it cannot display dialogs or request user input.
	"""
	try:
		# Safely remove config specification
		if config.conf.spec is not None:
			if "quick_notes" in config.conf.spec:
				del config.conf.spec["quick_notes"]
				logger.info("Removed quick_notes config specification")

		# Safely remove config values
		if config.conf is not None:
			if "quick_notes" in config.conf:
				del config.conf["quick_notes"]
				logger.info("Removed quick_notes configuration values")

		# Save configuration if possible
		if hasattr(config.conf, "save"):
			config.conf.save()
			logger.info("Configuration saved successfully")

		logger.info("Addon configuration cleanup completed successfully")
	except Exception as e:
		# Log but don't raise - errors here shouldn't block addon removal
		logger.exception(f"Error during uninstall cleanup: {e}")
