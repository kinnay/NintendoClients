
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.switch import ProdInfo, KeySet
from nintendo.nex import backend, authentication, \
	datastore_smm2 as datastore, settings
from nintendo.games import SMM2
from anynet import http
import anyio
import zlib

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1200 #12.0.0

# You can get your user id and password from
# su/baas/<guid>.dat in save folder 8000000000000010.

# Bytes 0x20 - 0x28 contain the user id in reversed
# byte order, and bytes 0x28 - 0x50 contain the
# password in plain text.

# Alternatively, you can set up a mitm on your Switch
# and extract them from the request to /1.0.0/login

BAAS_USER_ID = 0x0123456789abcdef # 16 hex digits
BAAS_PASSWORD = "..." # Should be 40 characters

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
PATH_KEYS = "/path/to/prod.keys"
PATH_PRODINFO = "/path/to/PRODINFO"

# Tickets can be dumped with nxdumptool.
# You need the base ticket, not an update ticket.
# Do not remove console specific data.
PATH_TICKET = "/path/to/ticket"

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %SMM2.GAME_SERVER_ID
PORT = 443


async def main():
	keys = KeySet.load(PATH_KEYS)
	info = ProdInfo(keys, PATH_PRODINFO)
	
	with open(PATH_TICKET, "rb") as f:
		ticket = f.read()
	
	cert = info.get_tls_cert()
	pkey = info.get_tls_key()
	
	dauth = DAuthClient(keys)
	dauth.set_certificate(cert, pkey)
	dauth.set_system_version(SYSTEM_VERSION)
	response = await dauth.device_token(dauth.BAAS)
	device_token = response["device_auth_token"]
	
	aauth = AAuthClient()
	aauth.set_system_version(SYSTEM_VERSION)
	response = await aauth.auth_digital(
		SMM2.TITLE_ID, SMM2.LATEST_VERSION,
		device_token, ticket
	)
	app_token = response["application_auth_token"]
	
	baas = BAASClient()
	baas.set_system_version(SYSTEM_VERSION)
	
	response = await baas.authenticate(device_token)
	access_token = response["accessToken"]
	
	response = await baas.login(
		BAAS_USER_ID, BAAS_PASSWORD, access_token, app_token
	)
	user_id = int(response["user"]["id"], 16)
	id_token = response["idToken"]
	
	auth_info = authentication.AuthenticationInfo()
	auth_info.token = id_token
	auth_info.ngs_version = 4 #Switch
	auth_info.token_type = 2
	
	s = settings.load("switch")
	s.configure(SMM2.ACCESS_KEY, SMM2.NEX_VERSION, SMM2.CLIENT_VERSION)
	async with backend.connect(s, HOST, PORT) as be:
		async with be.login(str(user_id), auth_info=auth_info) as client:
			# Search for ninji courses
			store = datastore.DataStoreClientSMM2(client)
			
			param = datastore.SearchCoursesEventParam()
			courses = await store.search_courses_event(param)
			print("Found %i ninji courses.\n" %len(courses))
			
			# Print information about the oldest ninji course
			course = courses[-1]
			print("Name:", course.name)
			print("Description:", course.description)
			print("Start time:", course.upload_time)
			print("End time:", course.end_time)
			print()
			
			# Request ghost info
			param = datastore.GetEventCourseGhostParam()
			param.data_id = course.data_id
			param.time = 30000 # Request ghosts with a time around 30 seconds
			param.count = 1 # Only request a single ghost
			
			ghost = (await store.get_event_course_ghost(param))[0]
			
			# Request info about the ghost player
			param = datastore.GetUsersParam()
			param.pids = [ghost.pid]
			
			user = (await store.get_users(param)).users[0]
			print("Player:", user.name)
			print("Time: %i.%03i" %(ghost.time // 1000, ghost.time % 1000))
			print()
			
			# Download replay file
			header_info = await store.get_req_get_info_headers_info(ghost.replay_file.data_type)
			headers = {h.key: h.value for h in header_info.headers}
			response = await http.get(ghost.replay_file.url, headers=headers)
			response.raise_if_error()
			
			# Decompress and save replay file
			data = zlib.decompress(response.body)
			with open("replay.bin", "wb") as f:
				f.write(data)

anyio.run(main)
