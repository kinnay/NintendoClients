
from nintendo.nex import backend, authentication, friends, common
from nintendo.games import Friends
from nintendo import account

import logging
logging.basicConfig(level=logging.INFO)

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4 #EUR
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


api = account.AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
api.set_title(Friends.TITLE_ID_EUR, Friends.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

pid = api.get_pid(USERNAME)
mii = api.get_mii(pid)

nex_token = api.get_nex_token(Friends.GAME_SERVER_ID)

backend = backend.BackEndClient("friends.cfg")
backend.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)

login_data = authentication.NintendoLoginData()
login_data.token = nex_token.token
backend.login(
	nex_token.username, nex_token.password,
	None, login_data
)

nna_info = friends.NNAInfo()
nna_info.principal_info.pid = pid
nna_info.principal_info.nnid = USERNAME
nna_info.principal_info.mii.name = mii.name
nna_info.principal_info.mii.data = mii.data.build()

#NintendoPresenceV2 tells the server about your online status, which
#game you're currently playing, etc. This will be shown to your friends
#in their friend list (unless you disabled this feature).	
presence = friends.NintendoPresenceV2()

client = friends.FriendsClient(backend.secure_client)
response = client.get_all_information(
	nna_info, presence,
	#Enter your birthday here
	common.DateTime.make(15, 11, 1999, 0, 0, 0)
)


def print_requests(requests):
	for request in requests:
		principal_info = request.principal_info
		message = request.message
		print("\tWho: %s (%s)" %(principal_info.nnid, principal_info.mii.name))
		print("\tMessage:", message.message)
		if message.game_key.title_id:
			print("\tGame: %016X (v%i)" %(message.game_key.title_id, message.game_key.title_version))
		print("\tSent:", request.sent)
		print("\tExpires:", message.expires)
		print("\t" + "-" * 40)
	print()


if response.comment.text:
	print("Your status message: %s (last changed on %s)" %(response.comment.text, response.comment.changed))
else:
	print("You don't have a status message")

if response.friends:
	print("Friends:")
	for friend in response.friends:
		principal_info = friend.nna_info.principal_info
		print("\tNNID:", principal_info.nnid)
		print("\tName:", principal_info.mii.name)
		
		presence = friend.presence
		print("\tOnline:", ["No", "Yes"][presence.is_online])
		if presence.game_key.title_id:
			print("\tPlaying: %016X (v%i)" %(presence.game_key.title_id, presence.game_key.title_version))
		
		if friend.comment.text:
			print("\tStatus: %s (last changed on %s)" %(friend.comment.text, friend.comment.changed))
			
		print("\tFriend since:", friend.befriended)
		print("\tLast online:", friend.last_online)
		print("\t" + "-" * 40)
	print()
else:
	print("You don't have any friends")

if response.sent_requests:
	print("Friend requests sent:")
	print_requests(response.sent_requests)
else:
	print("You haven't sent any friend requests")
	
if response.received_requests:
	print("Friend requests received:")
	print_requests(response.received_requests)
else:
	print("You haven't received any friend requests")
	
if response.blacklist:
	print("Blacklist:")
	for item in response.blacklist:
		principal_info = item.principal_info
		print("\tWho: %s (%s)" %(principal_info.nnid, principal_info.mii.name))
		if item.game_key.title_id:
			print("\tGame: %016X (%i)" %(item.game_key.title_id, item.game_key.title_version))
		print("\tSince:", item.since)
		print("\t" + "-" * 40)
else:
	print("You haven't blacklisted any users")


backend.close()
