# -*- coding: UTF-8 -*-
"""
NVDA Add-on: Quick Notes
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

logger = logging.getLogger("quick_notes.installTasks")

PANDOC_RELEASE_URL = "https://github.com/jgm/pandoc/releases/latest"


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
	"""Check if Pandoc is available and prompt user if not."""
	# Try to get user's pandoc path if config is available
	try:
		user_pandoc_path = config.conf["quick_notes"].get("pandocUserPath", "")
		show_prompt = config.conf["quick_notes"].get("showPandocPromptOnInstall", True)
	except (KeyError, AttributeError):
		# Config not initialized yet (will be done at runtime)
		user_pandoc_path = ""
		show_prompt = True

	if not show_prompt:
		return

	pandoc_path = locate_pandoc(user_pandoc_path)
	if pandoc_path:
		logger.info(f"Pandoc detected at {pandoc_path}.")
		return

	# Only import gui.message when needed
	try:
		from gui.message import MessageDialog, ReturnCode
	except ImportError:
		logger.error("Could not import gui.message. Pandoc prompt will not be shown.")
		return

	result = MessageDialog.ask(
		_(
			"Pandoc is required for Quick Notes to convert documents. Would you like to open the Pandoc releases page to download it?"
		),
		_("Pandoc Not Found"),
	)
	if result == getattr(ReturnCode, "YES", 1):
		import webbrowser

		webbrowser.open(PANDOC_RELEASE_URL)


def onUninstall():
	"""Clean up addon configuration when uninstalled.

	Following NVDA's standard pattern:
	- Remove spec definition only
	- Let NVDA handle the rest
	- User data (if any) is preserved by design
	"""
	try:
		# Remove spec only (this disables the addon's config in NVDA)
		if "quick_notes" in config.conf.spec:
			del config.conf.spec["quick_notes"]
			logger.info("Removed quick_notes config spec")

		# Save configuration
		config.conf.save()
		logger.info("Addon configuration cleanup completed")

	except Exception:
		logger.exception("Error during uninstall cleanup")
