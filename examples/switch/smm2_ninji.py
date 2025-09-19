
from nintendo.switch import dauth, aauth, baas, dragons
from nintendo.nex import backend, authentication, \
	settings, datastore_smm2 as datastore
from nintendo import switch
from anynet import http
import anyio
import zlib

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 2040 # 20.4.0

# You can get your user id and password from
# su/baas/<guid>.dat in save folder 8000000000000010.

# Bytes 0x20 - 0x28 contain the user id in reversed
# byte order, and bytes 0x28 - 0x50 contain the
# password in plain text.

# Alternatively, you can set up a mitm on your Switch
# and extract them from the request to /1.0.0/login

BAAS_USER_ID = 0x0123456789abcdef # 16 hex digits
BAAS_PASSWORD = "..." # Should be 40 characters
NA_COUNTRY = "JP" # Country of your Nintendo account

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
PATH_KEYS = "/path/to/prod.keys"
PATH_PRODINFO = "/path/to/PRODINFO"

# License information is stored encrypted in saved/<license owner id>
# in save folder 80000000000000E4.

# Alternatively, they can be obtained from the dragons server
# by calling publish_device_linked_elicenses (see docs), or with
# a mitm on your Switch.
ELICENSE_ID = "..." # 32 hex digits
NA_ID = 0x0123456789abcdef # 16 hex digits

PENNE_ID = "..."


TITLE_ID = 0x01009B90006DC000
TITLE_VERSION = 0x70000

GAME_SERVER_ID = 0x22306D00
ACCESS_KEY = "fdf6617f"
NEX_VERSION = 40605
CLIENT_VERSION = 60


HOST = "g%08x-lp1.s.n.srv.nintendo.net" %GAME_SERVER_ID
PORT = 443


async def main():
	keys = switch.load_keys(PATH_KEYS)
	
	info = switch.ProdInfo(keys, PATH_PRODINFO)
	cert = info.get_tls_cert()
	pkey = info.get_tls_key()
	
	dauth_client = dauth.DAuthClient(keys)
	dauth_client.set_certificate(cert, pkey)
	dauth_client.set_system_version(SYSTEM_VERSION)

	dauth_cache = dauth.DAuthCache(dauth_client)
	
	dragons_client = dragons.DragonsClient()
	dragons_client.set_certificate(cert, pkey)
	dragons_client.set_system_version(SYSTEM_VERSION)
	
	aauth_client = aauth.AAuthClient()
	aauth_client.set_certificate(cert, pkey)
	aauth_client.set_system_version(SYSTEM_VERSION)
	
	baas_client = baas.BAASClient()
	baas_client.set_system_version(SYSTEM_VERSION)
	
	# Request a device authentication token for dragons
	response = await dauth_cache.device_token(dauth.CLIENT_ID_DRAGONS)
	device_token_dragons = response["device_auth_token"]
	
	# Request a device authentication token for aauth and bass
	response = await dauth_cache.device_token(dauth.CLIENT_ID_BAAS)
	device_token_baas = response["device_auth_token"]
	
	# Request a contents authorization token from dragons
	response = await dragons_client.contents_authorization_token_for_aauth(device_token_dragons, ELICENSE_ID, NA_ID, TITLE_ID)
	contents_token = response["contents_authorization_token"]
	
	# Request an application authentication token
	response = await aauth_client.auth_digital(TITLE_ID, TITLE_VERSION, device_token_baas, contents_token)
	app_token = response["application_auth_token"]
	
	# Request an anonymous access token for baas
	response = await baas_client.authenticate(device_token_baas, PENNE_ID)
	access_token = response["accessToken"]
	
	# Log in on the baas server
	response = await baas_client.login(
		BAAS_USER_ID, BAAS_PASSWORD, access_token, app_token, NA_COUNTRY
	)
	user_id = int(response["user"]["id"], 16)
	id_token = response["idToken"]

	# Set up authentication info for nex server
	auth_info = authentication.AuthenticationInfo()
	auth_info.token = id_token
	auth_info.ngs_version = 4 #Switch
	auth_info.token_type = 2
	
	s = settings.load("switch")
	s.configure(ACCESS_KEY, NEX_VERSION, CLIENT_VERSION)
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
