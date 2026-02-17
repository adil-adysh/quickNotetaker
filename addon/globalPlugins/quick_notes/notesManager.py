# notesManager.py
# -*- coding: utf-8 -*-
# A part from Quick Notes add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from logHandler import log
from datetime import datetime
import json
from .constants import get_data_dir_path, get_data_file_path
from .helpers import getTitle


class note(object):
	"""A class that represents a single note"""

	def __init__(self, id="", title="", content="", lastEdited="", lastEditedStamp="", docxPath=""):
		if not id:
			self.id = datetime.now().strftime("%Y%m%d%H%M%S")
			self.title = getTitle(content)
			self.content = content
			self.lastEdited = self.prettyFormat(datetime.now())
			self.lastEditedStamp = datetime.now().strftime("%Y%m%d%H%M%S")
			self.docxPath = docxPath
		else:
			self.id = id
			self.title = title
			self.content = content
			self.lastEdited = lastEdited
			self.lastEditedStamp = lastEditedStamp
			self.docxPath = docxPath

	def updateNote(self, newContent, docxPath):
		if newContent is not None:  # and self.content != newContent:
			# for now, allow the user to edit the content even though the content hasn't changed to be able to overcome the title bug present in the first release
			self.title = getTitle(newContent)
			self.content = newContent
			self.lastEdited = self.prettyFormat(datetime.now())
			self.lastEditedStamp = datetime.now().strftime("%Y%m%d%H%M%S")
		if docxPath is not None and self.docxPath != docxPath:
			self.docxPath = docxPath

	def prettyFormat(self, datetime):
		return f"{datetime.strftime('%d')}/{datetime.strftime('%m')}/{datetime.strftime('%Y')}, {datetime.strftime('%H')}:{datetime.strftime('%M')}"


def initialize():
	data_file_path = get_data_file_path()
	data_dir_path = get_data_dir_path()
	if os.path.isfile(data_file_path):
		return
	log.debug(f"Creating a new file {os.path.abspath(data_file_path)}")
	try:
		if not os.path.isdir(data_dir_path):
			os.makedirs(data_dir_path, exist_ok=True)
	except Exception:
		log.error("Can't create the data file directory!")
		raise
	try:
		with open(data_file_path, mode="x", encoding="utf8") as file:
			file.write("[]")
	except FileExistsError:
		pass  # File was created by another process
	except Exception:
		log.error("Can't create data file")
		raise


def loadAllNotes():
	data_file_path = get_data_file_path()
	with open(data_file_path, mode="r", encoding="utf8") as file:
		allNotes = json.load(file, object_hook=deserializeNote)
	return allNotes


def deserializeNote(dict):
	deserializedNote = note(
		dict["id"],
		dict["title"],
		dict["content"],
		dict["lastEdited"],
		dict["lastEditedStamp"],
		dict["docxPath"],
	)
	return deserializedNote


def _dumpAllNotes(allNotes):
	data_file_path = get_data_file_path()
	# Backup the file content
	with open(data_file_path, mode="r", encoding="utf8") as file:
		allContent = file.read()
	# Sort all notes according to the last edited stamp in descending order
	allNotes.sort(key=lambda note: note.lastEditedStamp, reverse=True)
	try:
		with open(data_file_path, mode="w", encoding="utf8") as file:
			json.dump([note.__dict__ for note in allNotes], file, indent=4, ensure_ascii=False)
	except (IOError, OSError) as e:
		log.error(f"Failed to save notes: {e}")
		with open(data_file_path, mode="w", encoding="utf8") as file:
			file.write(allContent)
		raise


def saveNewNote(noteContent, docxPath=""):
	newNote = note(content=noteContent, docxPath=docxPath)
	allNotes = loadAllNotes()
	allNotes.append(newNote)
	_dumpAllNotes(allNotes)


def deleteNote(noteID):
	allNotes = loadAllNotes()
	for note in allNotes:
		if note.id == noteID:
			allNotes.remove(note)
			break
	_dumpAllNotes(allNotes)


def updateNote(noteID, newContent=None, docxPath=None):
	allNotes = loadAllNotes()
	for note in allNotes:
		if note.id == noteID:
			note.updateNote(newContent, docxPath)
			break
	_dumpAllNotes(allNotes)
