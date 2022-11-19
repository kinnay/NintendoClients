
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.dragons import DragonsClient
from nintendo.nex import backend, settings, authentication, datastore
from nintendo.games import GBG
from nintendo import switch
from anynet import http
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


GAME_CODE = "G 006 TR2 9JK"

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %GBG.GAME_SERVER_ID
PORT = 443


def code_to_data_id(code, access_key):
	if not code.startswith("G"):
		raise ValueError("Game code must start with G")
	
	charset = "0123456789BCDFGHJKLMNPRTVWXY"
	code = code.replace(" ", "")[1:]
	
	value = 0
	for char in code:
		value = value * len(charset) + charset.index(char)
	value ^= 0xDEAD9ED5
	
	data_id = ((value >> 32) << 24) | (value & 0xFFFFFF)
	
	key = 0
	for byte in access_key.encode():
		key ^= byte
		key = (key << 4) | (key >> 4)
		key &= 0xFF
	
	while value:
		key ^= value & 0xFF
		value >>= 8
		
	if key != 0:
		raise ValueError("Game code is invalid")
	return data_id


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
	response = await dragons.contents_authorization_token_for_aauth(device_token_dragons, ELICENSE_ID, NA_ID, GBG.TITLE_ID)
	contents_token = response["contents_authorization_token"]
	
	# Request an application authentication token
	response = await aauth.auth_digital(GBG.TITLE_ID, GBG.LATEST_VERSION, device_token_baas, contents_token)
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
	
	s = settings.load("switch")
	s.configure(GBG.ACCESS_KEY, GBG.NEX_VERSION, GBG.CLIENT_VERSION)
	async with backend.connect(s, HOST, PORT) as be:
		async with be.login(str(user_id), auth_info=auth_info) as client:
			store = datastore.DataStoreClient(client)
			
			# Request meta data
			param = datastore.DataStoreGetMetaParam()
			param.data_id = code_to_data_id(GAME_CODE)
			
			meta = await store.get_meta(param)
			print("Data id:", meta.data_id)
			print("Owner id:", meta.owner_id)
			print("Uploaded at:", meta.create_time)
			print("Expires at:", meta.expire_time)
			
			# Download game file
			result = await store.get_object_infos([meta.data_id])
			result.results[0].raise_if_error()
			
			info = result.infos[0]
			url = "https://" + info.url
			headers = {h.key: h.value for h in info.headers}
			response = await http.get(url, headers=headers)
			response.raise_if_error()
			with open("game.bin", "wb") as f:
				f.write(response.body)

anyio.run(main)
