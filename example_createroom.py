
from nintendo.nex import backend, authentication, friends, matchmaking, common
from nintendo.account import AccountAPI
from nintendo.games import MK8
import struct

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4 #EUR
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


#This function logs in on a game server
def backend_login(title, auth_info, login_data, settings=None):
	api.set_title(title.TITLE_ID_EUR, title.LATEST_VERSION)
	nex_token = api.get_nex_token(title.GAME_SERVER_ID)

	auth_info = None
	login_data = None
	if auth_info:
		auth_info = authentication.AuthenticationInfo(nex_token.token, title.SERVER_VERSION)
	if login_data:
		login_data = authentication.NintendoLoginData(nex_token.token)
	
	client = backend.BackEndClient(title.ACCESS_KEY, title.NEX_VERSION, settings)
	client.connect(nex_token.host, nex_token.port)
	client.login(
		nex_token.username, nex_token.password, auth_info
	)
	return client


api = AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
api.login(USERNAME, PASSWORD)

#Connect to both the Mario Kart 8 server and the Wii U friends server
friends_backend = backend_login(
	friends.FriendsTitle, False, True, backend.Settings("friends.cfg")
)
game_backend = backend_login(MK8, True, False)

pid = game_backend.get_pid()

friends_client = friends.FriendsClient(friends_backend)
matchmaker = matchmaking.MatchmakeExtensionClient(game_backend)

#Create a matchmake session
matchmake_session = matchmaking.MatchmakeSession(
	#Create a gathering with between 2 and 12 players
	#and the participation policy set to 98
	0, 0, 0, 2, 12, 98, 0, 0, 0, "",
	3, [0, 0, 0, 0, 0x403, 0], #game mode = 3, flags = 0x403 (DLCs enabled)
	True, #Open participation
	matchmaking.MatchmakeSystem.FRIENDS, #Only friends will join
	b"", 0, b"", 100, 0
)
session_id, session_key = matchmaker.create_matchmake_session(
	matchmake_session, "", 1
)

#Tell friends we're playing MK8 and have created a room
application_data = b"\0\0\x20\x03\0\0\0\0\0\0\0\0\x18" + struct.pack("<I", pid) + b"\0\0\0"
presence = friends.NintendoPresenceV2(
	0x1EE, True, friends.GameKey(MK8.TITLE_ID_EUR, MK8.LATEST_VERSION), 0,
	"I'm a Python client", 2, 2, MK8.GAME_SERVER_ID, 3,
	pid, session_id, application_data, 3, 3, 3
)
friends_client.update_presence(presence)

input("Press enter to disconnect and exit\n")

#Tell friends we've gone offline
presence = friends.NintendoPresenceV2(
	0, False, friends.GameKey(0, 0), 0, "", 0, 0, 0, 0, 0, 0, b"", 0, 0, 0
)
friends_client.update_presence(presence)

#Disconnect from servers
game_backend.close()
friends_backend.close()
