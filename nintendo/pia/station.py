
from nintendo.pia.common import StationAddress, InetAddress
from nintendo.pia.packet import PIAMessage
from nintendo.nex.common import StationUrl
from nintendo.common import signal
import collections
import struct
import random

import logging
logger = logging.getLogger(__name__)


class StationLocation(collections.namedtuple("StationLocation", "address pid cid rvcid url_type sid stream_type natm natf type probeinit")):
	fmt = ">IIIBBBBBBB"
	
	@classmethod
	def from_station_url(cls, url):
		inet_address = InetAddress(url["address"], url["port"])
		station_address = StationAddress(inet_address, 0)
		return cls(
			station_address, url["PID"], url["CID"], url["RVCID"], url.get_type_id(), url["sid"],
			url["stream"], url["natm"], url["natf"], url["type"], url["probeinit"]
		)
		
	def to_station_url(self):
		url = StationUrl()
		url.set_type_id(self.url_type)
		url["address"] = self.address.address.host
		url["port"] = self.address.address.port
		url["PID"] = self.pid
		url["CID"] = self.cid
		url["RVCID"] = self.rvcid
		url["sid"] = self.sid
		url["stream"] = self.stream_type
		url["natm"] = self.natm
		url["natf"] = self.natf
		url["type"] = self.type
		url["probeinit"] = self.probeinit
		return url
		
	@classmethod
	def deserialize(cls, data):
		address = StationAddress.deserialize(data)
		args = struct.unpack_from(cls.fmt, data, address.sizeof())
		return cls(address, *args)
		
	def serialize(self):
		return self.address.serialize() + struct.pack(self.fmt, *self[1:])

	@staticmethod
	def sizeof(): return StationAddress.sizeof() + 19

		
class StationConnectionInfo(collections.namedtuple("StationConnectionInfo", "public_station local_station")):
	@classmethod
	def deserialize(cls, data):
		loc1 = StationLocation.deserialize(data)
		loc2 = StationLocation.deserialize(data[loc1.sizeof():])
		return cls(loc1, loc2)
		
	def serialize(self):
		return self.public_station.serialize() + self.local_station.serialize()
		
	@staticmethod
	def sizeof(): return StationLocation.sizeof() * 2
		
		
class IdentificationInfo(collections.namedtuple("IdentificationInfo", "id name")):
	@classmethod
	def deserialize(cls, data):
		identification = data[:32].decode("ascii").rstrip("\0")
		name = data[32:64].decode("utf_16_be").rstrip("\0")
		return cls(identification, name)
		
	def serialize(self):
		data = self.id.encode("ascii").ljust(32, b"\0")
		data += self.name.encode("utf_16_be").ljust(32, b"\0")
		data += bytes([len(self.name), 0])
		return data
		
	@staticmethod
	def sizeof(): return 66
	
	
class Station:
	def __init__(self, address, rvcid):
		self.address = address
		self.rvcid = rvcid

		self.index = 0xFD
		self.sequence_id = 1
		self.connection_id = random.randint(2, 255)
		
		self.identification_info = None
		self.connection_info = None
		
		self.rtt_timer = None
		self.base_timer = None
		
		self.is_connected = False
		
	def inet_address(self):
		return InetAddress(self.address[0], self.address[1])
		
	def station_address(self):
		return StationAddress(self.inet_address(), 0)
	
	def next_sequence_id(self):
		result = self.sequence_id
		self.sequence_id += 1
		if self.sequence_id == 0x10000:
			self.sequence_id = 1
		return result
		
		
class StationTable:
	def __init__(self):
		self.stations = []
		
	def __iter__(self):
		return iter(self.stations)
		
	def create(self, address, rvcid):
		if self.find_by_address(address):
			raise ValueError("Station already exists with address %s" %address)
		if self.find_by_rvcid(rvcid):
			raise ValueError("Station already exists with rvcid %i" %rvcid)

		station = Station(address, rvcid)
		self.stations.append(station)
		return station
		
	def find_by_connection_info(self, info):
		rvcids = [info.local_station.rvcid, info.public_station.rvcid]
		for station in self.stations:
			if station.rvcid in rvcids:
				return station
		
	def find_by_address(self, address):
		for station in self.stations:
			if station.address == address:
				return station
			if station.connection_info.public_station.address.address == address or \
			   station.connection_info.local_station.address.address == address:
				return station
				
	def find_by_rvcid(self, rvcid):
		for station in self.stations:
			if station.rvcid == rvcid:
				return station

				
class StationProtocol:

	PROTOCOL_ID = 0x100
	
	PORT_UNRELIABLE = 0
	PORT_RELIABLE = 1
	
	MESSAGE_CONNECTION_REQUEST = 1
	MESSAGE_CONNECTION_RESPONSE = 2
	MESSAGE_DISCONNECTION_REQUEST = 3
	MESSAGE_DISCONNECTION_RESPONSE = 4
	MESSAGE_ACK = 5
	MESSAGE_RELAY_CONNECTION_REQUEST = 6
	MESSAGE_RELAY_CONNECTION_RESPONSE = 7
	
	on_connection_request = signal.Signal()
	on_connection_response = signal.Signal()
	on_connection_denied = signal.Signal()
	
	on_disconnection_request = signal.Signal()
	on_disconnection_response = signal.Signal()
	
	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		self.resender = session.resending_transport
		
		self.handlers = {
			self.MESSAGE_CONNECTION_REQUEST: self.handle_connection_request,
			self.MESSAGE_CONNECTION_RESPONSE: self.handle_connection_response,
			self.MESSAGE_DISCONNECTION_REQUEST: self.handle_disconnection_request,
			self.MESSAGE_DISCONNECTION_RESPONSE: self.handle_disconnection_response,
			self.MESSAGE_ACK: self.handle_ack
		}
		
		self.inverse_requests = {}
		self.connection_responses = {}
		
	def handle(self, station, message):
		if message.protocol_port == self.PORT_UNRELIABLE:
			message_type = message.payload[0]
			self.handlers[message_type](station, message.payload)
		else:
			logger.warning("Only unreliable station protocol is supported")
		
	def handle_connection_request(self, station, message):
		logger.info("Received connection request")
		
		if message[2] != 3:
			logger.warning("Unsupported version number found in connection request")
			self.send_deny_connection(station, 2)
			return
		
		connection_info = StationConnectionInfo.deserialize(message[4:])
		connection_id = message[1]
		is_inverse = message[3]

		self.send_ack(station, message)
		self.on_connection_request(station, connection_info, connection_id, is_inverse)
		
	def handle_connection_response(self, station, message):
		logger.info("Received connection response")
		if message[1]:
			self.on_connection_denied(station, message[1])
		else:
			identification_info = IdentificationInfo.deserialize(message[4:])
			self.send_ack(station, message)
			self.on_connection_response(station, identification_info)
			
	def handle_disconnection_request(self, station, message):
		logger.info("Received disconnection request")
		self.on_disconnection_request(station)
		
	def handle_disconnection_response(self, station, message):
		logger.info("Received disconnection response")
		self.on_disconnection_response(station)
		
	def handle_ack(self, station, message):
		self.resender.handle_ack(message)
		
	def send_connection_request(self, station, is_inverse=False):
		logger.debug("Sending connection request")
		data = bytes([self.MESSAGE_CONNECTION_REQUEST, self.session.station.connection_id, 3, is_inverse])
		data += self.session.station.connection_info.serialize()
		self.send(station, data, True)
		
	def send_connection_response(self, station):
		logger.debug("Sending connection response")
		data = bytes([self.MESSAGE_CONNECTION_RESPONSE, 0, 3, 3])
		data += self.session.station.identification_info.serialize()
		data += b"\0\0" #Alignment
		self.send(station, data, True)
		
	def send_deny_connection(self, station, reason):
		logger.debug("Denying connection request")
		data = bytes([self.MESSAGE_CONNECTION_RESPONSE, reason, 3, 0])
		self.send(station, data)
		
	def send_disconnection_request(self, station):
		logger.debug("Sending disconnection request")
		data = bytes([self.MESSAGE_DISCONNECTION_REQUEST])
		self.send(station, data)
		
	def send_disconnection_response(self, station):
		logger.debug("Sending disconnection response")
		data = bytes([self.MESSAGE_DISCONNECTION_RESPONSE])
		self.send(station, data)
		
	def send_ack(self, station, message):
		logger.debug("Sending ack message")
		ack_id = struct.unpack_from(">I", message, -4)[0]
		data = struct.pack(">BxxxI", self.MESSAGE_ACK, ack_id)
		self.send(station, data)
		
	def send(self, station, payload, ack=False):
		message = PIAMessage()
		message.flags = 0
		message.protocol_id = self.PROTOCOL_ID
		message.protocol_port = self.PORT_UNRELIABLE
		message.payload = payload
		if ack:
			self.resender.send(station, message)
		else:
			self.transport.send(station, message)

			
class StationMgr:

	station_connected = signal.Signal()
	station_disconnected = signal.Signal()
	connection_denied = signal.Signal()

	def __init__(self, session):
		self.protocol = session.station_protocol
		self.protocol.on_connection_request.add(self.handle_connection_request)
		self.protocol.on_connection_response.add(self.handle_connection_response)
		self.protocol.on_connection_denied.add(self.handle_connection_denied)
		self.protocol.on_disconnection_request.add(self.handle_disconnection_request)
		self.protocol.on_disconnection_response.add(self.handle_disconnection_response)
		
		self.stations = StationTable()
		
	def handle_connection_request(self, station, connection_info, connection_id, is_inverse):
		if station != self.stations.find_by_connection_info(connection_info):
			logger.warning("Unexpected station connection info found in connection request")
			self.protocol.send_deny_connection(station, 1)
			return
			
		station.connection_info = connection_info
		station.connection_id = connection_id
		
		if not is_inverse:
			self.protocol.send_connection_request(station, True)

		self.protocol.send_connection_response(station)
			
	def handle_connection_response(self, station, identification_info):
		logger.info("Station connected: %s" %identification_info.name)
		station.identification_info = identification_info
		station.is_connected = True
		self.station_connected(station)
			
	def handle_connection_denied(self, station, reason):
		self.connection_denied(station)
		
	def handle_disconnection_request(self, station):
		self.protocol.send_disconnection_response(station)
		
	def handle_disconnection_response(self, station):
		station.is_connected = False
		self.station_disconnected(station)
		
	def connect(self, station):
		if station.is_connected:
			self.station_connected(station)
		else:
			self.protocol.send_connection_request(station)
			
	def disconnect(self, station):
		if not station.is_connected:
			self.station_disconnected(station)
		else:
			self.protocol.send_disconnection_request(station)
		
	def create(self, address, rvcid): return self.stations.create(address, rvcid)
	
	def find_by_address(self, address):
		return self.stations.find_by_address(address)
	def find_by_connection_info(self, info):
		return self.stations.find_by_connection_info(info)
	def find_by_rvcid(self, rvcid):
		return self.stations.find_by_rvcid(rvcid)
