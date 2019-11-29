
from nintendo.nex import backend, authentication, notification
from nintendo.games import Friends
from nintendo import nnas

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


class NotificationServer(notification.NintendoNotificationServer):
	def __init__(self):
		super().__init__()
		self.name_cache = {}
		
	def process_nintendo_notification_event(self, context, event):
		pid = event.pid
		if pid not in self.name_cache:
			self.name_cache[pid] = api.get_nnid(pid)
		name = self.name_cache[pid]
		
		if event.type == notification.NintendoNotificationType.LOGOUT:
			print("%s is now offline" %name)

		elif event.type == notification.NintendoNotificationType.UNFRIENDED:
			print("%s removed you from his friend list" %name)

		elif event.type == notification.NintendoNotificationType.STATUS_CHANGE:
			print("%s changed his status message to: %s" %(name, event.data.text))
			
		elif event.type == notification.NintendoNotificationType.PRESENCE_CHANGE:
			presence = event.data
			game = "[%016X v%i]" %(presence.game_key.title_id, presence.game_key.title_version)
			message = presence.message
			if message:
				print("%s is playing %s (message: %s)" %(name, game, message))
			else:
				print("%s is playing %s" %(name, game))
				
		else:
			print("Unknown notification type %i (from %s)" %(event.type, name))
		
	def process_presence_change_event(self, context, event):
		self.process_nintendo_notification_event(context, event)


nnas = nnas.NNASClient()
nnas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
nnas.set_title(Friends.TITLE_ID_EUR, Friends.LATEST_VERSION)
nnas.login(USERNAME, PASSWORD)

nex_token = nnas.get_nex_token(Friends.GAME_SERVER_ID)
backend = backend.BackEndClient("friends.cfg")
backend.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)

login_data = authentication.NintendoLoginData()
login_data.token = nex_token.token
backend.login(
	nex_token.username, nex_token.password, None,
	login_data
)
backend.secure_client.register_server(NotificationServer())

input("Press enter to disconnect and exit\n")
backend.close()
