
from nintendo.pia.streams import StreamOut, StreamIn
from nintendo.pia.message import PIAMessage
from nintendo.pia.types import StationConnectionInfo, StationLocation, IdentificationInfo, PlayerInfo
from nintendo.pia.stations import ConnectionState
from nintendo.common import scheduler
import random

import logging
logger = logging.getLogger(__name__)


class StationProtocol:
	MESSAGE_CONNECTION_REQUEST = 1
	MESSAGE_CONNECTION_RESPONSE = 2
	MESSAGE_DISCONNECTION_REQUEST = 3
	MESSAGE_DISCONNECTION_RESPONSE = 4
	MESSAGE_ACK = 5
	MESSAGE_RELAY_CONNECTION_REQUEST = 6
	MESSAGE_RELAY_CONNECTION_RESPONSE = 7

	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		self.transport = session.transport
		self.resender = session.resender
		
		self.version = self.derive_version(self.settings)
		self.platform = self.derive_platform(self.settings)
		
		self.handlers = {
			self.MESSAGE_CONNECTION_REQUEST: self.handle_connection_request,
			self.MESSAGE_CONNECTION_RESPONSE: self.handle_connection_response,
			self.MESSAGE_ACK: self.handle_ack
		}
		
	def derive_version(self, settings):
		version = settings.get("pia.version") // 100
		if version == 306: return 2
		if version in [309, 310]: return 3
		if 408 <= version <= 410: return 5
		if version in [502, 503]: return 7
		if version == 509: return 8
		if 510 <= version <= 518: return 9
		raise ValueError("Unsupported PIA version: %i" %version)
		
	def derive_platform(self, settings):
		if settings.get("pia.version") >= 50000:
			return 4
		return 3
		
	def get_protocol_type(self):
		if self.settings.get("pia.protocol_type_revision") == 0:
			return 0x0100
		return 0x14
		
	def handle(self, station, message):
		message_type = message.payload[0]
		if message_type in self.handlers:
			self.handlers[message_type](station, message.payload)
		else:
			logger.warning("Unknown station protocol message: %i" %message_type)
			
	def handle_connection_request(self, station, data):
		logger.debug("Received connection request")
		
		stream = StreamIn(data, self.settings)
		stream.skip(1)
		
		connection_id = stream.u8()
		version = stream.u8()
		inverse = stream.bool()
		
		if version != self.version:
			logger.error("Received connection request with wrong version number")
			self.send_denying_connection_response(station, 2)
			return
		
		local_station = self.session.local_station()
		local_info = local_station.connection_info.local
		if self.version >= 7:
			if stream.pid() != local_info.pid:
				logger.error("Received connection request with wrong pid")
				return
		if self.version >= 8:
			if stream.u32() != local_info.cid:
				logger.error("Received connection request with wrong cid")
				return
			inverse_id = stream.u8()
			if inverse_id != station.connection_id_out_temp:
				logger.error("Received connection request with wrong inverse connection id: %i", inverse_id)
				return
		
		if self.version == 8:
			conn_info = stream.extract(StationConnectionInfo)
		else:
			location = stream.extract(StationLocation)
			conn_info = StationConnectionInfo(location)
			
		ack_id = stream.u32()
			
		if inverse:
			if station.connection_state != ConnectionState.WAIT_INVERSE_REQUEST:
				logger.error("Received unexpected inverse connection request")
				self.send_denying_connection_response(station, 1)
				return
			
			station.connection_id_in_temp = connection_id
			station.connection_info = conn_info
			
			self.send_ack(station, ack_id)
			self.send_connection_response(station)
			
			station.connection_state = ConnectionState.WAIT_RESPONSE
		else:
			if station.connection_state != ConnectionState.DISCONNECTED:
				logger.error("Received unexpected connection request")
				self.send_denying_connection_response(station, 1)
				return
			
			station.connection_id_out_temp = random.randint(2, 0xFF)
			station.connection_id_in_temp = connection_id
			station.connection_info = conn_info
			
			self.send_ack(station, ack_id)
			self.send_connection_request(station, connection_id)
			
			station.connection_state = ConnectionState.WAIT_INVERSE_RESPONSE
		
	def handle_connection_response(self, station, data):
		logger.debug("Received connection response")
		
		if station.connection_state not in [ConnectionState.WAIT_RESPONSE, ConnectionState.WAIT_INVERSE_RESPONSE]:
			logger.error("Received unexpected connection response")
			return
			
		stream = StreamIn(data, self.settings)
		stream.skip(1)
		
		identification = self.process_connection_response(stream)
		if identification is not None:
			ack_id = stream.u32()
			self.send_ack(station, ack_id)
			
			station.identification_info = identification
			if station.connection_state == ConnectionState.WAIT_INVERSE_RESPONSE:
				self.send_connection_response(station)
			station.connection_state = ConnectionState.CONNECTED
		else:
			station.connection_state = ConnectionState.ERROR
		
	def process_connection_response(self, stream):
		local_station = self.session.local_station()
		local_info = local_station.connection_info.local
		
		result = stream.u8()
		if result != 0:
			logger.error("Connection was denied: %i" %result)
			return None
			
		version = stream.u8()
		if version != self.version:
			logger.error("Connection response has unexpected version number")
			return None
			
		platform = stream.u8()
		if platform != self.platform:
			logger.error("Connection response has unexpected platform id")
			return None
			
		identification = IdentificationInfo()
		if self.version < 7:
			identification.token = stream.chars(32).split("\0")[0]
			
			player = PlayerInfo()
			player.name = stream.wchars(16)[:stream.u8()]
			player.language = stream.u8()
			identification.players.append(player)
		else:
			relay = stream.u8()
			if relay != 0:
				logger.error("Connection response has unexpected relay field")
				return None
			
			pid = stream.pid()
			if pid != local_info.pid:
				logger.error("Connection response has unexpected pid")
				return None
				
			cid = stream.u32()
			if cid != local_info.cid:
				logger.error("Connection response has unexpected cid")
				return None
				
			identification.token = stream.chars(32).split("\0")[0]
			
			session_id = stream.u32()
			if session_id != self.session.get_session_id():
				logger.error("Connection response has unexpected session id")
				return None
			
			num_players = stream.u8()
			identification.participants = stream.u8()
			num_player_infos = stream.u8()
			
			if num_players != num_player_infos:
				logger.error("Number of players is different from number of player infos")
				return None
				
			for i in range(num_player_infos):
				player = PlayerInfo()
				
				name_bytes = stream.read(80)
				name_encoding = stream.u8()
				if name_encoding == 1:
					player.name = name_bytes.decode("utf8")
				elif name_encoding == 2:
					player.name = name_bytes.decode("utf16")
				else:
					logger.error("Invalid player name encoding")
					return None
				
				nickname_bytes = stream.read(40)
				nickname_encoding = stream.u8()
				if nickname_encoding == 1:
					player.nickname = nickname_bytes.decode("utf8")
				elif nickname_encoding == 2:
					player.nickname = nickname_bytes.decode("utf16")
				else:
					logger.error("Invalid account name encoding")
					return None
				
				player.language = stream.u8()
				player.play_history_key = stream.read(64)
				player.info = stream.u64()
				
				identification.players.append(player)
				
			stream.pad((4 - num_player_infos) * 0xC3)
		
		if stream.available() != 4:
			logger.error("Connection response has unexpected size")
			return None
		return identification
	
	def handle_ack(self, station, data):
		logger.debug("Received ack")
		
		stream = StreamIn(data, self.settings)
		stream.skip(4)
		ack_id = stream.u32()
		
		self.resender.acknowledge(station, ack_id)

	def send_connection_request(self, station, inverse_id=None):
		logger.debug("Sending connection request")
		
		is_inverse = inverse_id is not None
		
		local = self.session.local_station()
		local_info = local.connection_info
		target_info = station.connection_info
	
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_CONNECTION_REQUEST)
		stream.u8(station.connection_id_out_temp)
		stream.u8(self.version)
		stream.bool(is_inverse)
		
		if self.version >= 7:
			stream.pid(target_info.local.pid)
		if self.version >= 8:
			stream.u32(target_info.local.cid)
			if is_inverse:
				stream.u8(inverse_id)
			else:
				stream.u8(0)
		
		if self.version == 8:
			stream.add(local_info)
		else:
			stream.add(local_info.local)
			
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		self.resender.send(station, message)
		
	def send_connection_response(self, station):
		logger.debug("Sending connection response")
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_CONNECTION_RESPONSE)
		stream.u8(0)
		stream.u8(self.version)
		stream.u8(self.platform)
		
		identification = self.session.local_station().identification_info
		
		if self.version < 7:
			stream.chars(identification.token.ljust(32, "\0"))
			
			player = identification.players[0]
			stream.wchars(player.name.ljust(16, "\0"))
			stream.u8(len(player.name))
			stream.u8(player.language)
		else:
			stream.u8(0)
			stream.u64(station.connection_info.local.pid)
			stream.u32(station.connection_info.local.cid)
			stream.chars(identification.token.ljust(32, "\0"))
			stream.u32(self.session.get_session_id())
			stream.u8(len(identification.players))
			stream.u8(identification.participants)
			stream.u8(len(identification.players))
			
			for player in identification.players:
				stream.write(player.name.encode("utf8").ljust(80, b"\0"))
				stream.u8(1)
				stream.write(player.nickname.encode("utf8").ljust(40, b"\0"))
				stream.u8(1)
				stream.u8(player.language)
				stream.write(player.play_history_key)
				stream.u64(player.info)
				
			stream.pad(0xC3 * (4 - len(identification.players)))
			
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
			
		self.resender.send(station, message)
		
	def send_denying_connection_response(self, station, reason):
		logger.debug("Sending denying connection response")
		
		target_location = station.connection_info.local
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_CONNECTION_RESPONSE)
		stream.u8(reason)
		stream.u8(self.version)
		stream.u8(0)
		if self.version >= 8:
			stream.u8(0)
			stream.u64(target_location.pid)
			stream.u32(target_location.cid)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		self.transport.send(station, message)
		
	def send_disconnection_request(self, station):
		logger.debug("Sending disconnection request")
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_DISCONNECTION_REQUEST)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		self.transport.send(station, message)
		
	def send_ack(self, station, ack_id):
		logger.debug("Acknowledging packet %i", ack_id)
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_ACK)
		stream.pad(3)
		stream.u32(ack_id)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		self.transport.send(station, message)
		
	def connect(self, station):
		if station.connection_state == ConnectionState.DISCONNECTED:
			station.connection_state = ConnectionState.WAIT_INVERSE_REQUEST
			station.connection_id_out_temp = random.randint(2, 0xFF)
		
			self.send_connection_request(station)
