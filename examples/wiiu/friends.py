
from nintendo.nex import backend, friends, common, settings
from nintendo import nnas
import anyio

import logging
logging.basicConfig(level=logging.INFO)


DEVICE_ID = 12345678 #From MCP_GetDeviceId
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x270
REGION = 4 #EUR
COUNTRY = "NL"
LANGUAGE = "en"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password

BIRTHDAY = common.DateTime.make(2000, 12, 31)

TITLE_ID = 0x10001C00
TITLE_VERSION = 0

GAME_SERVER_ID = 0x3200
ACCESS_KEY = "ridfebb9"
NEX_VERSION = 20000


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


async def main():
	nas = nnas.NNASClient()
	nas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
	nas.set_title(TITLE_ID, LATEST_VERSION)
	nas.set_locale(REGION, COUNTRY, LANGUAGE)
	
	access_token = await nas.login(USERNAME, PASSWORD)
	nex_token = await nas.get_nex_token(access_token.token, GAME_SERVER_ID)

	pid = await nas.get_pid(USERNAME)
	mii = await nas.get_mii(pid)
	
	s = settings.load("friends")
	s.configure(ACCESS_KEY, NEX_VERSION)
	async with backend.connect(s, nex_token.host, nex_token.port) as be:
		async with be.login(str(nex_token.pid), nex_token.password) as client:
			nna_info = friends.NNAInfo()
			nna_info.principal_info.pid = pid
			nna_info.principal_info.nnid = USERNAME
			nna_info.principal_info.mii.name = mii.name
			nna_info.principal_info.mii.data = mii.data
			
			#NintendoPresenceV2 tells the server about your online status, which
			#game you're currently playing, etc. This will be shown to your friends
			#in their friend list (unless you disabled this feature).	
			presence = friends.NintendoPresenceV2()
			
			friends_client = friends.FriendsClientV2(client)
			response = await friends_client.update_and_get_all_information(
				nna_info, presence, BIRTHDAY
			)
			
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

anyio.run(main)
			