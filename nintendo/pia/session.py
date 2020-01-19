
from nintendo.pia.proto.station import StationProtocol
from nintendo.pia.proto.mesh import MeshProtocol
from nintendo.pia.proto.lan import LanProtocol
from nintendo.pia.proto.unreliable import UnreliableProtocol
from nintendo.pia.types import StationConnectionInfo, StationLocation, StationAddress
from nintendo.pia.message import MessageTransport
from nintendo.pia.resender import ResendingTransport
from nintendo.pia.stations import StationTable, ConnectionState
from nintendo.pia.lan import LANServer, LanStationInfo
from nintendo.pia.mesh import Mesh
from nintendo.nex.matchmaking import MatchmakeSession, MatchmakeExtensionClient, MatchMakingClient
from nintendo.settings import Settings
from nintendo.common import scheduler, util
import secrets
import random
import socket
import struct
import hashlib
import hmac

import logging
logger = logging.getLogger(__name__)


class SessionSettings:
	def __init__(self):
		self.game_mode = 0
		self.session_type = 0
		self.attributes = [0] * 6
		
		self.min_participants = 1
		self.max_participants = 4
		
		self.application_data = b""


class PIASession:
	def __init__(self, settings=None):
		if isinstance(settings, Settings):
			self.settings = settings.copy()
		else:
			self.settings = Settings(settings)
		
		self.stations = StationTable()
		self.transport = MessageTransport(self)
		self.resender = ResendingTransport(self.transport)
		self.mesh = Mesh()
		
		self.session_key = None
		self.my_station = None
		
		self.session_settings = None
		
		self.protocols = {}
	
	def configure(self, version):
		self.settings.set("pia.version", version)
		self.settings.set("pia.station_extension", version < 50000)
		self.settings.set("pia.crypto_enabled", version >= 50900)
		if version >= 50900:
			self.settings.set("pia.encryption_method", 1)
			self.settings.set("pia.signature_method", 0)
		if version >= 51100:
			self.settings.set("pia.header_version", 4)
		if version >= 50900:
			self.settings.set("pia.protocol_type_revision", 1)
		self.settings.set("pia.message_version", self.derive_message_version(version))
		
	def derive_message_version(self, pia_version):
		major_version = pia_version // 100
		if major_version <= 503: return 0
		if major_version in [509, 510]: return 1
		if major_version == 511: return 2
		if 514 <= major_version <= 517: return 3
		if major_version == 518: return 4
		raise ValueError("Unsupported PIA version: %i" %pia_version)
		
	def register_protocol(self, protocol):
		self.protocols[protocol.get_protocol_type()] = protocol
		
	def create_protocols(self):
		self.station_protocol = StationProtocol(self)
		self.mesh_protocol = MeshProtocol(self)
		self.unreliable_protocol = UnreliableProtocol(self)
		
		self.register_protocol(self.station_protocol)
		self.register_protocol(self.mesh_protocol)
		self.register_protocol(self.unreliable_protocol)
		
	def get_protocol(self, type):
		return self.protocols[type]
	
	def prepare(self, identification_info):
		logger.info("Initializing PIA session")
		self.create_protocols()
		
		self.transport.prepare()
		
		location = self.prepare_station_location()
		
		connection_info = StationConnectionInfo(location)
		
		self.my_station = self.stations.create()
		self.my_station.connection_state = ConnectionState.CONNECTED
		self.my_station.address = self.transport.local_address()
		self.my_station.connection_info = connection_info
		self.my_station.identification_info = identification_info
		self.my_station.id = self.build_station_id()
		
		self.event = scheduler.add_socket(self.handle_recv, self.transport)
		
	def cleanup(self):
		scheduler.remove(self.event)
		self.transport.cleanup()
	
	def create_mesh(self, session_key, settings):
		self.session_key = session_key
		self.session_settings = settings
		
		self.mesh.create(self.my_station)
		
	def join_mesh(self, session_key, host_location):
		self.session_key = session_key
		
		connection_info = StationConnectionInfo(host_location)
		
		address = host_location.local.address
		host = self.stations.create()
		host.address = address.host, address.port
		host.connection_info = connection_info
		self.connect_station(host)
		host.wait_connected()
		
		self.mesh_protocol.join(host)
		
	def leave_mesh(self):
		pass
		
	def connect_station(self, station):
		self.station_protocol.connect(station)
		
	def handle_recv(self, pair):
		station, message = pair
		
		protocol_id = message.protocol_id
		if protocol_id in self.protocols:
			self.protocols[protocol_id].handle(station, message)
		else:
			logger.warning("Unknown protocol id: 0x%X" %protocol_id)
		
	def get_mesh(self): return self.mesh
	def get_station_table(self): return self.stations
		
	def local_station(self): return self.my_station
	def host_station(self):
		index = self.mesh.get_host_index()
		return self.stations.find_by_index(index)
		
	def is_host(self):
		return self.local_station() == self.host_station()
		
	def get_game_mode(self): return self.session_settings.game_mode
	def get_attributes(self): return self.session_settings.attributes
	def get_num_participants(self): return self.mesh.get_num_participants()
	def get_min_participants(self): return self.session_settings.min_participants
	def get_max_participants(self): return self.session_settings.max_participants
	def get_session_type(self): return self.session_settings.session_type
	def get_application_data(self): return self.session_settings.application_data
	
	def get_session_key(self):
		return self.session_key
	def set_session_key(self, key):
		self.session_key = key

	def join(self, session): raise NotImplementedError
	def create(self): raise NotImplementedError
	def leave(self): raise NotImplementedError
		
	def generate_nonce(self, packet):
		raise NotImplementedError
	def get_session_id(self):
		raise NotImplementedError
	def build_station_id(self):
		raise NotImplementedError
		
		
class NEXSession(PIASession):
	def __init__(self, settings, backend):
		super().__init__(settings)
		self.backend = backend
		
		self.matchmake_ext = MatchmakeExtensionClient(backend.secure_client)
		self.matchmaker = MatchMakingClient(backend.secure_client)
		
	def join(self, session):
		key = self.matchmake_ext.join_matchmake_session(
			session.id, "Hello!"
		)
		url = self.matchmaker.get_session_urls(session.id)[0]
		location = StationLocation()
		location.set_station_url(url)
		self.join_mesh(key, location)
	
	def create(self, settings):
		session = MatchmakeSession()
		session.session_key = secrets.token_bytes(16)
		self.create_mesh(session.session_key, settings)
		
	def leave(self):
		self.leave_mesh()
		
	def create_protocols(self):
		super().create_protocols()
		
		self.nat_protocol = NATTraversalProtocol(self)
		
		self.register_protocol(self.nat_protocol)
		
	def prepare_station_location(self):
		location = StationLocation()
		location.set_station_url(self.backend.local_station)
		return location
		
	def get_session_id(self):
		return self.gathering.id
	
	def generate_nonce(self, packet):
		prefix = (packet.connection_id << 24) | (self.gathering_id & 0xFFFFFF)
		return prefix + struct.pack(">Q", packet.nonce)
		
	def build_station_id(self):
		return backend.local_station["RVCID"]


class LANSession(PIASession):
	def __init__(self, settings, key):
		super().__init__(settings)
		
		self.server = LANServer(settings, key)
		
		self.game_key = key
		
	def configure(self, version, app_version=0):
		super().configure(version)
		self.settings.set("pia.system_version", self.system_version(version))
		self.settings.set("pia.application_version", app_version)
		self.settings.set("pia.lan_version", self.server.lan_version(version))
		self.server.configure(version)
		
	def system_version(self, version):
		version = version // 100
		if version <= 503: return 0
		if version == 509: return 5
		if version == 510: return 6
		if version >= 511: return 7
		raise ValueError("Unsupported PIA version")
		
	def generate_session_key(self, param):
		param = param[:31] + bytes([(param[31] + 1) & 0xFF])
		return hmac.HMAC(self.game_key, param, hashlib.sha256).digest()[:16]
		
	def update_session_info(self):
		info = self.server.session_info
		info.game_mode = self.get_game_mode()
		info.attributes = self.get_attributes()
		info.num_participants = self.get_num_participants()
		info.min_participants = self.get_min_participants()
		info.max_participants = self.get_max_participants()
		info.system_version = self.settings.get("pia.system_version")
		info.application_version = self.settings.get("pia.application_version")
		info.session_type = self.get_session_type()
		info.application_data = self.get_application_data()
		info.is_opened = True
		
		host = self.host_station()
		info.host_location = host.connection_info.local
		
		info.stations = [LanStationInfo() for i in range(16)]
		for i, station in enumerate(self.mesh.stations):
			if station == host:
				info.stations[i].role = LanStationInfo.HOST
			else:
				info.stations[i].role = LanStationInfo.PLAYER
			player = station.identification_info.players[0]
			info.stations[i].username = player.nickname
			info.stations[i].id = station.id
		
	def join(self, session_info):
		self.server.session_info = session_info
		
		key = self.generate_session_key(session_info.session_param)
		host = session_info.host_location
		self.join_mesh(key, host)
	
	def create(self, settings):
		param = secrets.token_bytes(32)
		key = self.generate_session_key(param)
		self.server.session_info.session_param = param
		self.server.session_info.session_id = self.generate_session_id()
		self.create_mesh(key, settings)
		
		self.update_session_info()
		self.server.start()
		
	def leave(self):
		self.server.stop()
		self.leave_mesh()
	
	def create_protocols(self):
		super().create_protocols()
		
		self.lan_protocol = LanProtocol(self)
		
		self.register_protocol(self.lan_protocol)
		
	def get_session_info(self):
		return self.server.session_info
		
	def get_session_id(self):
		return self.get_session_info().session_id
		
	def prepare_station_location(self):
		host = util.local_address()
		port = self.transport.local_address()[1]
		
		location = StationLocation()
		location.local = StationAddress(host, port)
		location.pid = self.get_principal_id()
		location.cid = random.randint(0, 0xFFFFFFFF)
		location.rvcid = self.generate_session_id()
		location.type = 0
		return location
		
	def generate_nonce(self, packet):
		host = socket.inet_aton(packet.address[0])
		nonce = struct.pack(">Q", packet.nonce)
		return host + bytes([packet.connection_id]) + nonce[1:]
		
	def generate_session_id(self):
		address = self.transport.local_address()
		data = socket.inet_aton(address[0]) + struct.pack(">H", address[1])
		return struct.unpack_from(">I", data, 2)[0]
		
	def get_principal_id(self):
		address = self.transport.local_address()
		data = socket.inet_aton(address[0]) + struct.pack(">I", address[1])
		return struct.unpack(">Q", data)[0]
		
	def build_station_id(self):
		host, port = self.transport.local_address()
		data = socket.inet_aton(host) + struct.pack(">I", port)
		return struct.unpack(">Q", data)[0]
