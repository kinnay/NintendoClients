
from nintendo.pia.streams import StreamOut, StreamIn
from nintendo.pia.message import PIAMessage
from nintendo.pia.types import StationConnectionInfo, StationLocation
from nintendo.pia.mesh import JoinState
from nintendo.common import scheduler
import time

import logging
logger = logging.getLogger(__name__)


class StationInfo:
	def __init__(self):
		self.connection_info = None
		self.index = None
		
	def decode(self, stream):
		if stream.settings.get("pia.version") < 51000:
			self.connection_info = stream.extract(StationConnectionInfo)
		else:
			substream = StreamIn(stream.read(0x3E), stream.settings)
			location = substream.extract(StationLocation)
			self.connection_info = StationConnectionInfo(location)
		self.index = stream.u8()
		stream.align(4)
		
	def encode(self, stream):
		if stream.settings.get("pia.version") < 51000:
			stream.add(self.connection_info)
		else:
			substream = StreamOut(stream.settings)
			substream.add(self.connection_info.local)
			substream.pad(0x3E - substream.size())
			stream.write(substream.get())
		stream.u8(self.index)
		stream.align(4)


class JoinResponseParser:
	def __init__(self):
		self.num_stations = None
		self.host_index = None
		self.join_index = None
		self.num_fragments = None
		
		self.error = False
		
	def complete(self):
		if self.num_stations is None:
			return False
		return all(self.fragments) or self.error
		
	def update(self, stream):
		if self.error:
			logger.info("Ignoring join response because of a previous error")
			return False
		
		num_stations = stream.u8()
		host_index = stream.u8()
		join_index = stream.u8()
		num_fragments = stream.u8()
		
		if self.num_stations is None:
			self.num_stations = num_stations
			self.host_index = host_index
			self.join_index = join_index
			self.num_fragments = num_fragments
			
			self.stations = [None] * self.num_stations
			self.fragments = [False] * self.num_fragments
		else:
			if self.num_stations != num_stations or \
			   self.host_index != host_index or \
			   self.join_index != join_index or \
			   self.num_fragments != num_fragments:
				logger.error("Join response fragment has different header")
				self.error = True
				return False
				
		fragment_idx = stream.u8()
		fragment_size = stream.u8()
		fragment_base = stream.u8()
		
		if stream.settings.get("pia.version") >= 40000:
			stream.skip(4)
		if stream.settings.get("pia.version") >= 50000:
			stream.skip(4)
		
		if fragment_idx >= self.num_fragments:
			logger.error("Fragment index out of range")
			self.error = True
			return False
		
		if fragment_base + fragment_size > self.num_stations:
			logger.error("Fragment size out of range")
			self.error = True
			return False
		
		infos = []
		for i in range(fragment_size):
			infos.append(stream.extract(StationInfo))
			
		if stream.available() != 4:
			logger.error("Join response has unexpected size")
			self.error = True
			return False
		
		if self.fragments[fragment_idx]:
			logger.info("Ignoring fragment because we received it before")
			return True
			
		for i in range(fragment_size):
			if self.stations[fragment_base + i] is not None:
				logger.error("Fragments overlap")
				self.error = True
				return False
				
			self.stations[fragment_base + i] = infos[i]
			
		self.fragments[fragment_idx] = True
		
		if all(self.fragments):
			if not all(self.stations):
				logger.error("Join response is incomplete")
				self.error = True
				return False
		
		return True


class MeshProtocol:
	PORT_UNRELIABLE = 0
	PORT_RELIABLE = 1
	
	MESSAGE_JOIN_REQUEST = 0x1
	MESSAGE_JOIN_RESPONSE = 0x2
	MESSAGE_LEAVE_REQUEST = 0x4
	MESSAGE_LEAVE_RESPONSE = 0x8
	MESSAGE_DESTROY_MESH = 0x10
	MESSAGE_DESTROY_RESPONSE = 0x11
	MESSAGE_UPDATE_MESH = 0x20
	MESSAGE_KICKOUT_NOTICE = 0x21
	MESSAGE_DUMMY = 0x22
	MESSAGE_DUMMY_ACK = 0x23
	MESSAGE_CONNECTION_FAILURE = 0x24
	MESSAGE_GREETING = 0x40
	MESSAGE_MIGRATION_FINISH = 0x41
	MESSAGE_GREETING_RESPONSE = 0x42
	MESSAGE_MIGRATION_START = 0x44
	MESSAGE_MIGRATION_RESPONSE = 0x48
	MESSAGE_MULTI_MIGRATION_START = 0x49
	MESSAGE_MULTI_MIGRATION_RANK_DECISION = 0x4A
	MESSAGE_CONNECTION_REPORT = 0x80
	MESSAGE_RELAY_ROUTE_DIRECTIONS = 0x81

	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		self.transport = session.transport
		self.resender = session.resender
		self.stations = session.stations
		self.mesh = session.mesh
		
		self.station_protocol = session.station_protocol
		
		self.handlers = {
			self.MESSAGE_JOIN_REQUEST: self.handle_join_request,
			self.MESSAGE_JOIN_RESPONSE: self.handle_join_response
		}
		
		self.join_response_parser = None
	
	def get_protocol_type(self):
		if self.settings.get("pia.protocol_type_revision") == 0:
			return 0x0200
		return 0x18
		
	def handle(self, station, message):
		if message.protocol_port == self.PORT_UNRELIABLE:
			message_type = message.payload[0]
			if message_type in self.handlers:
				self.handlers[message_type](station, message.payload)
			else:
				logger.warning("Unknown mesh protocol message: %i" %message_type)
		else:
			logger.error("Reliable mesh protocol is not supported")
			
	def handle_join_request(self, station, data):
		logger.debug("Received join request")
		
		logger.error("Join request is not implemented")
	
	def handle_join_response(self, station, data):
		logger.debug("Received join response")
		
		if self.join_response_parser is None:
			logger.error("Received unexpected join response")
			return
		
		if data[1] == 0:
			reason = data[4]
			logger.error("Join request was denied: %i", reason)
			self.join_response_parser.error = True
			return
		
		stream = StreamIn(data, self.settings)
		stream.skip(1)
		
		if self.join_response_parser.update(stream):
			ack_id = stream.u32()
			self.station_protocol.send_ack(station, ack_id)
	
	def send_join_request(self, station):
		logger.debug("Sending join request")
		
		local_station = self.session.local_station()
		local_address = local_station.connection_info.local.local
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_JOIN_REQUEST)
		stream.u8(local_station.index)
		
		if self.settings.get("pia.version") >= 51100:
			stream.pad(2)
			stream.add(local_address)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.protocol_port = self.PORT_UNRELIABLE
		message.payload = stream.get()
		
		self.resender.send(station, message)
		
	def join(self, host, timeout=3):
		if self.mesh.join_state == JoinState.NONE:
			parser = JoinResponseParser()
			
			self.join_response_parser = parser
			self.mesh.join_state = JoinState.JOINING
			self.send_join_request(host)
			
			start = time.monotonic()
			while not parser.complete():
				if time.monotonic() - start > timeout:
					raise RuntimeError("Timeout joining mesh")
				scheduler.update()
				
			if parser.error:
				raise RuntimeError("Failed to join mesh")
			
			self.mesh.set_host_index(parser.host_index)
			
			for info in parser.stations:
				address = info.connection_info.local.local.address
				station = self.stations.find_by_address((address.host, address.port), True)
				self.mesh.add_station(station, info.index)
			
			host.connection_id_in = host.connection_id_in_temp
			host.connection_id_out = host.connection_id_out_temp
			
			self.join_response_parser = None
			
			self.mesh.join_state = JoinState.WAIT_CONNECTIONS
			for station in self.mesh.get_stations():
				station.wait_connected()