
from nintendo.pia.packet import PIAMessage
from nintendo.common import scheduler, signal

import logging
logger = logging.getLogger(__name__)


class KeepAliveProtocol:

	PROTOCOL_ID = 0xC0
	
	on_receive = signal.Signal()

	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		
	def send(self, station):
		logger.debug("Sending keep alive packet")
		message = PIAMessage()
		message.flags = 0
		message.protocol_id = self.PROTOCOL_ID
		message.protocol_port = 0
		message.payload = b""
		self.transport.send(station, message)
		
	def handle(self, station, message):
		self.on_receive(station)
		
		
class KeepAliveMgr:
	def __init__(self, session):
		self.protocol = session.keep_alive_protocol

		self.mesh_mgr = session.mesh_mgr
		self.mesh_mgr.station_joined.add(self.handle_station_joined)
		
		self.keep_alive_send = [None] * 32
		
	def handle_station_joined(self, station):
		self.keep_alive_send[station.index] = \
			scheduler.add_timeout(self.send, 1, True, station)
			
	def send(self, station):
		self.protocol.send(station)
