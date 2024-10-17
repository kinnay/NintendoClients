
from nintendo.switch import sun, atumn
from nintendo import switch
import anyio
import os
import re
import struct
import subprocess


SYSTEM_VERSION = 1900 #19.0.0

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
PATH_KEYS = "/path/to/prod.keys"
PATH_PRODINFO = "/path/to/PRODINFO"

# This script uses hactool to parse NCA files
PATH_HACTOOL = "/path/to/hactool"

# Name of folder where files will be stored
OUTPUT_PATH = "/path/to/folder"


async def retry(worker, n=3):
	# If the download / connection fails, retry just in case
	for i in range(n):
		try:
			return await worker
		except anyio.BrokenResourceError:
			print("Retrying...")
	raise Exception("Download failed!")

async def download_content_metadata(atumn_client, title_id, title_version, *, system_update=False):
	# Download NCA
	print("Downloading metadata NCA for title %016x..." %title_id)
	data = await retry(atumn_client.download_content_metadata(title_id, title_version, system_update=system_update))
	
	# Save data to file
	nca_path = OUTPUT_PATH + "/metadata_nca/%016x.nca" %title_id
	with open(nca_path, "wb") as f:
		f.write(data)
	
	# Extract CNMT from NCA
	section0dir = OUTPUT_PATH + "/cnmt"
	output = subprocess.check_output([PATH_HACTOOL, nca_path, "--section0dir", section0dir, "--disablekeywarns"])
	return re.search("\nSaving .* to (.*)\\.\\.\\.\n", output.decode())[1] # Return the filename

async def download_content(atumn_client, title_id, metadata_path):
	# Parse the CNMT
	with open(metadata_path, "rb") as f:
		data = f.read()
	
	content_count = struct.unpack_from("<H", data, 0x10)[0]
	if content_count == 0: return # Nothing to do
	elif content_count > 1:
		raise ValueError("We currently assume that each title has no more than one NCA")
	
	# Download content NCA
	content_id = data[0x40:0x50].hex()
	content_size = struct.unpack_from("<I", data, 0x50)[0]

	print("Downloading content NCA for title %016x... (%i bytes)" %(title_id, content_size))
	data = await retry(atumn_client.download_content(content_id))

	# Save data to file
	nca_path = OUTPUT_PATH + "/content_nca/%016x.nca" %title_id
	with open(nca_path, "wb") as f:
		f.write(data)
	
	# Unpacking content NCA
	content_path = OUTPUT_PATH + "/titles/%016x" %title_id
	os.makedirs(content_path, exist_ok=True)

	exefsdir = content_path + "/exefs"
	romfsdir = content_path + "/romfs"

	args = [
		PATH_HACTOOL, nca_path, "--exefsdir", exefsdir,
		"--romfsdir", romfsdir, "--disablekeywarns"
	]
	subprocess.run(args, stdout=subprocess.DEVNULL)

	# Rename folder if there is a name in the NPDM
	npdm_path = content_path + "/exefs/main.npdm"
	if os.path.isfile(npdm_path):
		with open(npdm_path, "rb") as f:
			name = f.read()[0x20:0x30].rstrip(b"\0").decode()
			if name != "Application":
				os.rename(content_path, OUTPUT_PATH + "/titles/%s" %name)


async def main():
	keys = switch.load_keys(PATH_KEYS)
	
	prodinfo = switch.ProdInfo(keys, PATH_PRODINFO)
	device_cert = prodinfo.get_tls_cert()
	device_cert_key = prodinfo.get_tls_key()
	device_id = prodinfo.get_device_id()
	
	sun_client = sun.SunClient(device_id)
	sun_client.set_system_version(SYSTEM_VERSION)
	sun_client.set_certificate(device_cert, device_cert_key)

	atumn_client = atumn.AtumnClient(device_id)
	atumn_client.set_system_version(SYSTEM_VERSION)
	atumn_client.set_certificate(device_cert, device_cert_key)

	# Prepare folders
	os.makedirs(OUTPUT_PATH + "/metadata_nca", exist_ok=True)
	os.makedirs(OUTPUT_PATH + "/content_nca", exist_ok=True)
	os.makedirs(OUTPUT_PATH + "/cnmt", exist_ok=True)
	os.makedirs(OUTPUT_PATH + "/titles", exist_ok=True)

	# Request latest system update info
	response = await sun_client.system_update_meta()
	title_id = int(response["system_update_metas"][0]["title_id"], 16)
	title_version = response["system_update_metas"][0]["title_version"]

	print("Latest system update:")
	print("    Title id: %016x" %title_id)
	print("    Title version: %i" %title_version)
	print()

	# Download metadata NCA for the system update title
	await download_content_metadata(atumn_client, title_id, title_version, system_update=True)

	# Parse CNMT of the system update title
	with open(OUTPUT_PATH + "/cnmt/SystemUpdate_%016x.cnmt" %title_id, "rb") as f:
		data = f.read()
	
	titles = []
	metadata_count = struct.unpack_from("<H", data, 0x12)[0]
	for i in range(metadata_count):
		title_id, title_version = struct.unpack_from("<QI", data, 0x24 + i * 0x10)
		titles.append((title_id, title_version))
	
	# Download and unpack remaining metadata NCAs
	metadata_paths = {}
	for title_id, title_version in titles:
		metadata_path = await download_content_metadata(atumn_client, title_id, title_version)
		metadata_paths[title_id] = metadata_path
	
	# Download and unpack content NCAs
	for title_id, path in metadata_paths.items():
		await download_content(atumn_client, title_id, path)
		

anyio.run(main)
