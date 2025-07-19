# -*- coding: UTF-8 -*-
"""
NVDA Add-on: quickNotetaker
installTasks to check for Pandoc in system path and guide the user to download if not found.
"""

import addonHandler
import gettext
import shutil
import webbrowser
import wx
from logHandler import log

addonHandler.initTranslation()
log.info("quickNotetaker: installTasks.py module loaded.")

PANDOC_RELEASE_URL = "https://github.com/jgm/pandoc/releases/latest"

_ = gettext.gettext

class PandocInstallDialog(wx.Dialog):
    def __init__(self, parent=None):
        super().__init__(parent, title=_("Pandoc Not Found"), style=wx.DEFAULT_DIALOG_STYLE)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        explanation = (
            _("Pandoc is required for QuickNotetaker to convert documents.\n\n") +
            _("You can install Pandoc easily using Windows Package Manager (winget).\n") +
            _("Click the button below to copy the install command to your clipboard.\n\n") +
            _("Alternatively, you can visit the Pandoc releases page to download manually, or choose to install Pandoc later.")
        )
        sizer.Add(wx.StaticText(panel, label=explanation), flag=wx.ALL, border=10)

        copyBtn = wx.Button(panel, label=_("Copy 'winget install pandoc' to clipboard"))
        sizer.Add(copyBtn, flag=wx.ALL | wx.EXPAND, border=10)
        copyBtn.Bind(wx.EVT_BUTTON, self.onCopy)

        openBtn = wx.Button(panel, label=_("Open Pandoc Releases Page"))
        sizer.Add(openBtn, flag=wx.ALL | wx.EXPAND, border=10)
        openBtn.Bind(wx.EVT_BUTTON, self.onOpen)

        laterBtn = wx.Button(panel, label=_("Install Pandoc Later"))
        sizer.Add(laterBtn, flag=wx.ALL | wx.EXPAND, border=10)
        laterBtn.Bind(wx.EVT_BUTTON, self.onLater)

        panel.SetSizer(sizer)
        sizer.Fit(panel)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def onCopy(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject("winget install pandoc"))
            wx.TheClipboard.Close()
            wx.MessageBox(_("Command copied to clipboard!"), _("Info"), wx.OK | wx.ICON_INFORMATION)

    def onOpen(self, event):
        webbrowser.open(PANDOC_RELEASE_URL)

    def onLater(self, event):
        self.Close()

def onInstall():
    log.info("quickNotetaker: Running onInstall to check Pandoc availability.")

    if shutil.which("pandoc"):
        log.info("quickNotetaker: Pandoc detected in system PATH.")
        return

    app = wx.GetApp() or wx.App(False)
    dlg = PandocInstallDialog()
    dlg.ShowModal()
