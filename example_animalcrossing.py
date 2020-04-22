
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.switch import ProdInfo, KeySet, TicketList
from nintendo.nex import backend, authentication, matchmaking
from nintendo.games import ACNH

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1001 #10.0.1

# You can get your username and password from
# su/baas/<guid>.dat in save folder 8000000000000010.

# Bytes 0x20 - 0x28 contain the user id in reversed
# byte order, and bytes 0x28 - 0x50 contain the
# password in plain text.

# Alternatively, you can set up a mitm on your Switch
# and extract them from the request to /1.0.0/login

BAAS_USERNAME = "0123456789abcdef" # 16 hex digits
BAAS_PASSWORD = "..." # Should be 40 characters

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
keys = KeySet("/path/to/prod.keys")
info = ProdInfo(keys, "/path/to/PRODINFO")

# Tickets can be dumped with nxdumptool.
# You need the base ticket, not an update ticket.
with open("/path/to/ticket", "rb") as f:
	ticket = f.read()

CODE = "ABCDE" # Dodo code


HOST = "g%08x-lp1.s.n.srv.nintendo.net" %ACNH.GAME_SERVER_ID
PORT = 443

cert = info.get_ssl_cert()
pkey = info.get_ssl_key()


# Request a dauth token
dauth = DAuthClient(keys)
dauth.set_certificate(cert, pkey)
dauth.set_system_version(SYSTEM_VERSION)
response = dauth.device_token()
device_token = response["device_auth_token"]

# Request an aauth token
aauth = AAuthClient()
response = aauth.auth_digital(
	ACNH.TITLE_ID, ACNH.TITLE_VERSION,
	device_token, ticket
)
app_token = response["application_auth_token"]

# Log in on baas server
baas = BAASClient()
baas.authenticate(device_token)
response = baas.login(BAAS_USERNAME, BAAS_PASSWORD, app_token)

user_id = int(response["user"]["id"], 16)
id_token = response["idToken"]

# Connect to game server
backend = backend.BackEndClient("switch.cfg")
backend.configure(ACNH.ACCESS_KEY, ACNH.NEX_VERSION, ACNH.CLIENT_VERSION)
backend.connect(HOST, PORT)

# Log in on game server
auth_info = authentication.AuthenticationInfo()
auth_info.token = id_token
auth_info.ngs_version = 4 #Switch
auth_info.token_type = 2
backend.login(str(user_id), auth_info=auth_info)

mm = matchmaking.MatchmakeExtensionClient(backend.secure_client)

param = matchmaking.MatchmakeSessionSearchCriteria()
param.attribs = ["", "", "", "", "", ""]
param.game_mode = "2"
param.min_players = "1"
param.max_players = "1,8"
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

sessions = mm.browse_matchmake_session_no_holder_no_result_range(param)
if not sessions:
	print("\nNo island found for '%s'\n" %CODE)
else:
	session = sessions[0]
	data = session.application_data
	print("\nFound island:")
	print("\tId:", session.id)
	print("\tActive players:", session.player_count)
	print("\tIsland name:", data[12:32].decode("utf16"))
	print()

# Disconnect from game server
backend.close()
