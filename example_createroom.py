
from nintendo.nex import backend, authentication, friends, matchmaking, common
from nintendo.nnas import NNASClient
from nintendo.games import MK8, Friends
import struct

import logging
logging.basicConfig(level=logging.INFO)

#Device id can be retrieved from MCP_GetDeviceId
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x250
REGION = 4 #EUR
COUNTRY = "NL"
LANGUAGE = "en"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


#This function logs in on a game server
def backend_login(title, use_auth_info, use_login_data, settings=None):
	nnas.set_title(title.TITLE_ID_EUR, title.LATEST_VERSION)
	nex_token = nnas.get_nex_token(title.GAME_SERVER_ID)

	auth_info = None
	login_data = None
	if use_auth_info:
		auth_info = authentication.AuthenticationInfo()
		auth_info.token = nex_token.token
		auth_info.server_version = title.SERVER_VERSION
	if use_login_data:
		login_data = authentication.NintendoLoginData()
		login_data.token = nex_token.token
	
	client = backend.BackEndClient(settings)
	client.configure(title.ACCESS_KEY, title.NEX_VERSION)
	client.connect(nex_token.host, nex_token.port)
	client.login(
		nex_token.username, nex_token.password, auth_info, login_data
	)
	return client


nnas = NNASClient()
nnas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
nnas.set_locale(REGION, COUNTRY, LANGUAGE)
nnas.login(USERNAME, PASSWORD)

#Connect to both the Mario Kart 8 server and the Wii U friends server
friends_backend = backend_login(
	Friends, False, True, "friends.cfg"
)
game_backend = backend_login(MK8, True, False)

pid = game_backend.get_pid()

friends_client = friends.FriendsClient(friends_backend.secure_client)
matchmaker = matchmaking.MatchmakeExtensionClient(game_backend.secure_client)

#Create a matchmake session
matchmake_session = matchmaking.MatchmakeSession()
matchmake_session.player_min = 2
matchmake_session.player_max = 12
matchmake_session.participation_policy = 98
matchmake_session.game_mode = 3
matchmake_session.attribs[4] = 0x403 #DLCs enabled
matchmake_session.matchmake_system = matchmaking.MatchmakeSystem.FRIENDS

session_id = matchmaker.create_matchmake_session(
	matchmake_session, "", 1
).gid

#Tell friends we're playing MK8 and have created a room
application_data = b"\0\0\x20\x03\0\0\0\0\0\0\0\0\x18" + struct.pack("<I", pid) + b"\0\0\0"

presence = friends.NintendoPresenceV2()
presence.flags = 0x1EE
presence.is_online = True
presence.game_key.title_id = MK8.TITLE_ID_EUR
presence.game_key.title_version = MK8.LATEST_VERSION
presence.message = "I'm a Python client"
presence.unk2 = 2
presence.unk3 = 2
presence.game_server_id = MK8.GAME_SERVER_ID
presence.unk4 = 3
presence.pid = pid
presence.gathering_id = session_id
presence.application_data = application_data

friends_client.update_presence(presence)

input("Press enter to disconnect and exit\n")

#Tell friends we've gone offline
presence = friends.NintendoPresenceV2()
friends_client.update_presence(presence)

#Disconnect from servers
game_backend.close()
friends_backend.close()
