
from nintendo.nex.nintendo_notification import NotificationType
from nintendo.nex.friends import FriendsTitle
from nintendo.nex.backend import BackEndClient
from nintendo.common.scheduler import Scheduler
from nintendo.act import AccountAPI


#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4 #EUR
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


name_cache = {}
def notification_callback(notification):
	pid = notification.pid
	if pid not in name_cache:
		name_cache[pid] = api.get_nnid(pid)
	name = name_cache[pid]
	
	if notification.type == NotificationType.LOGOUT:
		print("%s is now offline" %name)

	elif notification.type == NotificationType.UNFRIENDED:
		print("%s removed you from his friend list" %name)

	elif notification.type == NotificationType.STATUS_CHANGE:
		print("%s changed his status message to: %s" %(name, notification.object.text))
		
	elif notification.type == NotificationType.PRESENCE_CHANGE:
		presence = notification.object
		game = "[%016X v%i]" %(presence.game_key.title_id, presence.game_key.title_version)
		description = presence.description
		if description:
			print("%s is playing %s (description: %s)" %(name, game, description))
		else:
			print("%s is playing %s" %(name, game))


api = AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
api.set_title(FriendsTitle.TITLE_ID_EUR, FriendsTitle.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

scheduler = Scheduler()
scheduler.start()

nex_token = api.get_nex_token(FriendsTitle.GAME_SERVER_ID)
backend = BackEndClient(FriendsTitle.ACCESS_KEY, FriendsTitle.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password, nex_token.token)

backend.nintendo_notification_server.set_callback(notification_callback)

input("Press enter to disconnect and exit script\n")

backend.close()
scheduler.stop()



