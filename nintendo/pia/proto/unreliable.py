
from nintendo.pia.message import PIAMessage

import logging
logger = logging.getLogger(__name__)


class UnreliableProtocol:
	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		self.transport = session.transport
	
	def get_protocol_type(self):
		if self.settings.get("pia.protocol_type_revision") == 0:
			return 0x2000
		return 0x68
		
	def handle(self, station, message):
		logger.debug("Received %i bytes" %len(message.payload))
