
from nintendo.nex import nat, notification, nintendo_notification, authentication, secure, friends, common, settings


class BackEndClient:
	def __init__(self, game_server_id, access_key, version, config=None):
		self.game_server_id = game_server_id
		self.access_key = access_key.encode("ascii")
		self.version = version

		self.settings = config
		if not config:
			self.settings = settings.Settings()
		
		self.auth_client = None
		self.secure_client = None
		
		self.nat_traversal_server = nat.NATTraversalServer()
		self.notification_server = notification.NotificationServer()
		self.nintendo_notification_server = nintendo_notification.NintendoNotificationServer()

		self.protocol_map = {
			self.nat_traversal_server.PROTOCOL_ID: self.nat_traversal_server,
			self.notification_server.PROTOCOL_ID: self.notification_server,
			self.nintendo_notification_server.PROTOCOL_ID: self.nintendo_notification_server
		}
		
	def connect(self, host, port):
		self.auth_client = authentication.AuthenticationClient(self, self.access_key)
		self.auth_client.connect(host, port)
		
	def close(self):
		self.auth_client.close()
		if self.secure_client:
			self.secure_client.close()
		
	def login(self, username, password, auth_info=None):
		if auth_info and self.version != friends.FriendsTitle.NEX_VERSION:
			self.auth_client.login_ex(username, password, auth_info)
		else:
			self.auth_client.login(username, password)

		ticket = self.auth_client.request_ticket()
		host = self.auth_client.secure_station["address"]
		port = self.auth_client.secure_station["port"]
		
		self.secure_client = secure.SecureClient(self, self.access_key, ticket, self.auth_client)
		self.secure_client.connect(host, port)
		if self.version == friends.FriendsTitle.NEX_VERSION:
			urls = self.secure_client.register_urls(auth_info)
		else:
			urls = self.secure_client.register_urls()
		self.local_station, self.public_station = urls
		
	def login_guest(self):
		self.login("guest", "MMQea3n!fsik")
