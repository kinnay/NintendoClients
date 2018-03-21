
from nintendo.nex import backend, authentication, friends, nintendo_notification
from nintendo import account

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4 #EUR
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


class NotificationHandler(nintendo_notification.NintendoNotificationHandler):
	def __init__(self):
		self.name_cache = {}

	def process_notification_event(self, event):
		pid = event.pid
		if pid not in self.name_cache:
			self.name_cache[pid] = api.get_nnid(pid)
		name = self.name_cache[pid]
		
		if event.type == nintendo_notification.NotificationType.LOGOUT:
			print("%s is now offline" %name)

		elif event.type == nintendo_notification.NotificationType.UNFRIENDED:
			print("%s removed you from his friend list" %name)

		elif event.type == nintendo_notification.NotificationType.STATUS_CHANGE:
			print("%s changed his status message to: %s" %(name, event.data.text))
			
		elif event.type == nintendo_notification.NotificationType.PRESENCE_CHANGE:
			presence = event.data
			game = "[%016X v%i]" %(presence.game_key.title_id, presence.game_key.title_version)
			description = presence.description
			if description:
				print("%s is playing %s (description: %s)" %(name, game, description))
			else:
				print("%s is playing %s" %(name, game))

api = account.AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
api.set_title(friends.FriendsTitle.TITLE_ID_EUR, friends.FriendsTitle.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

nex_token = api.get_nex_token(friends.FriendsTitle.GAME_SERVER_ID)
backend = backend.BackEndClient(
	friends.FriendsTitle.ACCESS_KEY,
	friends.FriendsTitle.NEX_VERSION,
	backend.Settings("friends.cfg")
)
backend.connect(nex_token.host, nex_token.port)
backend.login(
	nex_token.username, nex_token.password,
	authentication.NintendoLoginData(nex_token.token)
)
backend.nintendo_notification_server.handler = NotificationHandler()

input("Press enter to disconnect and exit\n")
backend.close()
