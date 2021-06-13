
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.switch import ProdInfo, KeySet
from nintendo.nex import backend, settings, authentication, datastore
from nintendo.games import GBG
from anynet import http
import anyio

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1203 #12.0.3

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
		GBG.TITLE_ID, GBG.LATEST_VERSION,
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
