
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.dragons import DragonsClient
from nintendo.nex import backend, authentication, matchmaking, settings
from nintendo.games import ACNH
from nintendo import switch
import anyio

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1501 #15.0.1

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

# These can be obtained by calling publish_device_linked_elicenses (see docs)
# or with a mitm on your Switch (this is probably safer)
ELICENSE_ID = "..." # 32 hex digits
NA_ID = 0x0123456789abcdef # 16 hex digits


CODE = "ABCDE" # Dodo code

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %ACNH.GAME_SERVER_ID
PORT = 443


async def main():
	keys = switch.load_keys(PATH_KEYS)
	
	info = switch.ProdInfo(keys, PATH_PRODINFO)
	cert = info.get_tls_cert()
	pkey = info.get_tls_key()
	
	dauth = DAuthClient(keys)
	dauth.set_certificate(cert, pkey)
	dauth.set_system_version(SYSTEM_VERSION)
	
	dragons = DragonsClient()
	dragons.set_certificate(cert, pkey)
	dragons.set_system_version(SYSTEM_VERSION)
	
	aauth = AAuthClient()
	aauth.set_system_version(SYSTEM_VERSION)
	
	baas = BAASClient()
	baas.set_system_version(SYSTEM_VERSION)
	
	# Request a device authentication token for dragons
	response = await dauth.device_token(dauth.DRAGONS)
	device_token_dragons = response["device_auth_token"]
	
	# Request a device authentication token for aauth and bass
	response = await dauth.device_token(dauth.BAAS)
	device_token_baas = response["device_auth_token"]
	
	# Request a contents authorization token from dragons
	response = await dragons.contents_authorization_token_for_aauth(device_token_dragons, ELICENSE_ID, NA_ID, ACNH.TITLE_ID)
	contents_token = response["contents_authorization_token"]
	
	# Request an application authentication token
	response = await aauth.auth_digital(ACNH.TITLE_ID, ACNH.LATEST_VERSION, device_token_baas, contents_token)
	app_token = response["application_auth_token"]
	
	# Request an anonymous access token for baas
	response = await baas.authenticate(device_token_baas)
	access_token = response["accessToken"]
	
	# Log in on the baas server
	response = await baas.login(
		BAAS_USER_ID, BAAS_PASSWORD, access_token, app_token
	)
	user_id = int(response["user"]["id"], 16)
	id_token = response["idToken"]
	
	# Set up authentication info for nex server
	auth_info = authentication.AuthenticationInfo()
	auth_info.token = id_token
	auth_info.ngs_version = 4 #Switch
	auth_info.token_type = 2
	
	# Establish connection with nex server
	s = settings.load("switch")
	s.configure(ACNH.ACCESS_KEY, ACNH.NEX_VERSION, ACNH.CLIENT_VERSION)
	async with backend.connect(s, HOST, PORT) as be:
		async with be.login(str(user_id), auth_info=auth_info) as client:
			mm = matchmaking.MatchmakeExtensionClient(client)

			param = matchmaking.MatchmakeSessionSearchCriteria()
			param.attribs = ["", "", "", "", "", ""]
			param.game_mode = "2"
			param.min_participants = "1"
			param.max_participants = "1,8"
			param.matchmake_system = "1"
			param.vacant_only = False
			param.exclude_locked = True
			param.exclude_non_host_pid = True
			param.selection_method = 0
			param.vacant_participants = 1
			param.exclude_user_password = True
			param.exclude_system_password = True
			param.refer_gid = 0
			param.codeword = CODE

			sessions = await mm.browse_matchmake_session_no_holder_no_result_range(param)
			if not sessions:
				print("\nNo island found for '%s'\n" %CODE)
			else:
				session = sessions[0]
				data = session.application_data
				print("\nFound island:")
				print("\tId:", session.id)
				print("\tActive players:", session.num_participants)
				print("\tIsland name:", data[12:32].decode("utf16").rstrip("\0"))
				print("\tHost name:", data[40:60].decode("utf16").rstrip("\0"))
				print()

anyio.run(main)
