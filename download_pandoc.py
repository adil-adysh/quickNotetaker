"""
Script to download the latest Pandoc Windows binary and place it in the NVDA add-on structure.
"""

import urllib.request
import zipfile
import os
import stat
import json

# Define destination directory and binary path
PANDOC_DEST_DIR = os.path.join("addon", "globalPlugins", "quick_notes", "lib", "pandoc")
PANDOC_EXE_PATH = os.path.join(PANDOC_DEST_DIR, "pandoc.exe")


def download_latest_pandoc():
	"""
	Fetches the latest Pandoc release from GitHub, downloads the Windows binary,
	extracts pandoc.exe, and places it in the add-on directory.
	"""
	os.makedirs(PANDOC_DEST_DIR, exist_ok=True)
	print("Fetching latest Pandoc release info from GitHub...")
	api_url = "https://api.github.com/repos/jgm/pandoc/releases/latest"
	with urllib.request.urlopen(api_url) as response:
		release_info = json.load(response)
	asset_url = None
	for asset in release_info["assets"]:
		if "windows-x86_64.zip" in asset["name"]:
			asset_url = asset["browser_download_url"]
			asset_name = asset["name"]
			print(f"Found Pandoc asset: {asset_name}")
			break
	if not asset_url:
		raise RuntimeError("Could not find Pandoc Windows binary in the latest release.")
	archive_path = os.path.join(PANDOC_DEST_DIR, asset_name)
	print(f"Downloading Pandoc from: {asset_url}")
	urllib.request.urlretrieve(asset_url, archive_path)
	print(f"Extracting pandoc.exe to {PANDOC_DEST_DIR}")
	manual_extracted = False
	pandoc_extracted = False
	with zipfile.ZipFile(archive_path, "r") as zip_ref:
		for member in zip_ref.namelist():
			# Extract pandoc.exe
			if member.endswith("pandoc.exe") and not pandoc_extracted:
				zip_ref.extract(member, PANDOC_DEST_DIR)
				extracted_path = os.path.join(PANDOC_DEST_DIR, member)
				os.replace(extracted_path, PANDOC_EXE_PATH)
				parent_dir = os.path.dirname(extracted_path)
				if parent_dir != PANDOC_DEST_DIR:
					try:
						os.rmdir(parent_dir)
					except OSError:
						pass
				pandoc_extracted = True
			# Extract MANUAL.html
			if member.endswith("MANUAL.html") and not manual_extracted:
				zip_ref.extract(member, PANDOC_DEST_DIR)
				manual_path = os.path.join(PANDOC_DEST_DIR, member)
				manual_flat_path = os.path.join(PANDOC_DEST_DIR, "MANUAL.html")
				os.replace(manual_path, manual_flat_path)
				parent_dir = os.path.dirname(manual_path)
				if parent_dir != PANDOC_DEST_DIR:
					try:
						os.rmdir(parent_dir)
					except OSError:
						pass
				manual_extracted = True
			if pandoc_extracted and manual_extracted:
				break
	os.remove(archive_path)
	st = os.stat(PANDOC_EXE_PATH)
	os.chmod(PANDOC_EXE_PATH, st.st_mode | stat.S_IEXEC)
	print(f"Pandoc is ready at {PANDOC_EXE_PATH}")


if __name__ == "__main__":
	download_latest_pandoc()
