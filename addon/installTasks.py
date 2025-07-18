# -*- coding: UTF-8 -*-
"""
NVDA Add-on: quickNotetaker
installTasks to check for Pandoc in system path and guide the user to download if not found.
"""

import addonHandler
import gettext
import shutil
import webbrowser
from logHandler import log
from gui.message import MessageDialog, ReturnCode

addonHandler.initTranslation()
log.info("quickNotetaker: installTasks.py module loaded.")

PANDOC_RELEASE_URL = "https://github.com/jgm/pandoc/releases/latest"

# Use translation function _ from gettext
_ = gettext.gettext

def onInstall():
    log.info("quickNotetaker: Running onInstall to check Pandoc availability.")

    if shutil.which("pandoc"):
        log.info("quickNotetaker: Pandoc detected in system PATH.")
        return

    message = (
        _("Pandoc is not detected on your system. Pandoc is required for QuickNotetaker to convert documents.\n\n") +
        _("Note: Pandoc does not officially provide Windows ARM64 binaries. You may try the x86_64 version under emulation, or build Pandoc from source for ARM64.\n\n") +
        _("Would you like to open the Pandoc releases page to learn more or download available versions?")
    )
    title = _("Pandoc Not Found")

    userChoice = MessageDialog.ask(message, title)

    if userChoice == ReturnCode.YES:
        log.info(f"quickNotetaker: Opening Pandoc releases page: {PANDOC_RELEASE_URL}")
        webbrowser.open(PANDOC_RELEASE_URL)
    else:
        log.info("quickNotetaker: User declined to open the Pandoc download page.")
