
from nintendo.switch import dauth, aauth, baas, dragons
from nintendo.nex import backend, authentication, matchmaking, settings
from nintendo import switch
import anyio

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

CODE = "ABCDE" # Dodo code


TITLE_ID = 0x01006F8002326000
TITLE_VERSION = 0x1C0000

GAME_SERVER_ID = 0x2EE2E300
ACCESS_KEY = "v43a10em"
NEX_VERSION = 40604
CLIENT_VERSION = 2


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
	
	# Establish connection with nex server
	s = settings.load("switch")
	s.configure(ACCESS_KEY, NEX_VERSION, CLIENT_VERSION)
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
