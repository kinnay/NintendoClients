
class Settings:

	TRANSPORT_UDP = 0
	TRANSPORT_TCP = 1
	TRANSPORT_WEBSOCKET = 2

	def __init__(self):
		self.transport_type = self.TRANSPORT_UDP
		self.prudp_version = 1
		self.stream_type = 10
		
		self.fragment_size = 1300
		self.resend_timeout = 1.5
		self.ping_timeout = 4
		self.silence_timeout = 7.5
