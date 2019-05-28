
from nintendo.pia.common import StationAddress
from nintendo.pia.station import StationConnectionInfo
from nintendo.pia.transport import ReliableTransport
from nintendo.pia.packet import PIAMessage
from nintendo.common import scheduler, signal
import collections
import struct

import logging
logger = logging.getLogger(__name__)


class StationList:
	def __init__(self):
		self.stations = [None] * 32
	
	def add(self, station, index=None):
		if index is None:
			index = self.next_index()
			
		if not self.is_usable(index):
			raise IndexError("Tried to assign station to occupied index")

		station.index = index
		self.stations[index] = station
		
	def is_usable(self, index):
		return self.stations[index] is None
		
	def next_index(self):
		if None not in self.stations:
			raise OverflowError("A mesh can only hold up to 32 stations at once")
		return self.stations.index(None)
		
	def __len__(self):
		return 32 - self.stations.count(None)
		
	def __getitem__(self, index):
		filtered = list(filter(None, self.stations))
		return filtered[index]
		
	def __contains__(self, station):
		return station in self.stations

		
class StationInfo:
	def __init__(self):
		self.connection_info = None
		self.index = None
		
	def decode(self, stream):
		self.connection_info = stream.extract(StationConnectionInfo)
		self.index = stream.u8()
		stream.u8()
		
	def encode(self, stream):
		stream.add(self.connection_info)
		stream.u8(self.index)
		stream.u8(0)

		
class JoinResponseDecoder:

	finished = signal.Signal()

	def __init__(self):
		self.reset()
		
	def reset(self):
		self.station = None
		
	def parse(self, station, message):
		if self.station is None:
			self.update_info(station, message)
		elif not self.check_info(station, message):
			logger.warning("Incompatible join response fragment received")
			self.reset()
			self.update_info(station, message)
			
		fragment_index = message[5]
		if not self.fragments_received[fragment_index]:
			self.fragments_received[fragment_index] = True
			
			fragment_length = message[6]
			fragment_offs = message[7]
			
			offset = 8
			for i in range(fragment_length):
				index = fragment_offs + i
				
				if self.infos[index]:
					logger.warning("Overlapping join response fragments received")
				
				info = StationInfo.deserialize(message[offset:])
				offset += StationInfo.sizeof()
				self.infos[index] = info
				
			if all(self.infos):
				self.finished(station, self.host_index, self.assigned_index, self.infos)
				self.reset()

	def update_info(self, station, message):
		self.station = station
		self.num_stations = message[1]
		self.host_index = message[2]
		self.assigned_index = message[3]
		self.num_fragments = message[4]
		self.fragments_received = [False] * self.num_fragments
		self.infos = [None] * self.num_stations
		
	def check_info(self, station, message):
		return self.station == station and \
		       self.num_stations == message[1] and \
			   self.host_index == message[2] and \
			   self.assigned_index == message[3] and \
			   self.num_fragments == message[4]


class MeshProtocol:

	PROTOCOL_ID = 0x200
	
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
	
	on_join_request = signal.Signal()
	on_join_response = signal.Signal()
	on_join_denied = signal.Signal()
	
	on_leave_request = signal.Signal()
	on_leave_response = signal.Signal()
	
	on_destroy_request = signal.Signal()
	on_destroy_response = signal.Signal()
	
	on_mesh_update = signal.Signal()

	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		self.resender = session.resending_transport
		self.station_protocol = session.station_protocol
		
		self.handlers = {
			self.MESSAGE_JOIN_REQUEST: self.handle_join_request,
			self.MESSAGE_JOIN_RESPONSE: self.handle_join_response,
			self.MESSAGE_LEAVE_REQUEST: self.handle_leave_request,
			self.MESSAGE_LEAVE_RESPONSE: self.handle_leave_response,
			self.MESSAGE_DESTROY_MESH: self.handle_destroy_mesh,
			self.MESSAGE_DESTROY_RESPONSE: self.handle_destroy_response,
			self.MESSAGE_UPDATE_MESH: self.handle_update_mesh
		}
		
		self.sliding_windows = [None] * 32
		
		self.join_response_decoder = JoinResponseDecoder()
		self.join_response_decoder.finished.add(self.on_join_response)
		
	def assign_sliding_window(self, station):
		self.sliding_windows[station.index] = ReliableTransport(
			self.transport, station, self.PROTOCOL_ID,
			self.PORT_RELIABLE, self.handle_message
		)
	
	def handle(self, station, message):
		if message.protocol_port == self.PORT_UNRELIABLE:
			self.handle_message(station, message.payload)
		elif message.protocol_port == self.PORT_RELIABLE:
			if station.index == 0xFD:
				logger.warning("Received reliable mesh packet from unknown station")
			else:
				transport = self.sliding_windows[station.index]
				transport.handle(message)
		else:
			logger.warning("Unknown MeshProtocol port: %i", packet.protocol_port)
				
	def handle_message(self, station, message):
		message_type = message[0]
		self.handlers[message_type](station, message)

	def handle_join_request(self, station, message):
		station_address = StationAddress.deserialize(message[4:])
		station_index = message[1]
		self.station_protocol.send_ack(station, message)
		self.on_join_request(station, station_index, station_address)
		
	def handle_join_response(self, station, message):
		if message[1] == 0:
			self.on_join_denied(station, message[4])
		else:
			self.station_protocol.send_ack(station, message)
			self.join_response_decoder.parse(station, message)
			
	def handle_leave_request(self, station, message):
		station_address = StationAddress.deserialize(message[4:])
		station_index = message[1]
		self.on_leave_request(station, station_index, station_address)
		
	def handle_leave_response(self, station, message):
		station_address = StationAddress.deserialize(message[4:])
		station_index = message[1]
		self.on_leave_response(station, station_index, station_address)
			
	def handle_destroy_mesh(self, station, message):
		station_address = StationAddress.deserialize(message[4:])
		station_index = message[1]
		self.on_destroy_request(station, station_index, station_address)
		
	def handle_destroy_response(self, station, message):
		station_index = message[1]
		self.on_destroy_response(station, station_index)
			
	def handle_update_mesh(self, station, message):
		length = message[1]
		
		infos = []
		offset = 12
		for i in range(length):
			info = StationInfo.deserialize(message[offset:])
			offset += StationInfo.sizeof()
			infos.append(info)
			
		self.on_mesh_update(infos)
			
	def send_join_request(self, station):
		logger.info("Sending join request")
		
		data = bytes([
			self.MESSAGE_JOIN_REQUEST, self.session.station.index, 0, 0
		])
		data += self.session.station.station_address().serialize()

		self.send(station, data, 0, True)
		
	def send_join_response(self, station, assigned_index, host_index, stations):
		logger.info("Sending join response")

		infosize = (StationConnectionInfo.sizeof() + 4) & ~3
		limit = self.transport.size_limit() - 0xC
		
		per_packet = limit // infosize
		fragments = (len(stations) + per_packet - 1) // per_packet
		
		for i in range(fragments):
			offset = i * per_packet
			remaining = len(stations) - offset
			num_infos = min(remaining, per_packet)
			
			data = bytes([
				self.MESSAGE_JOIN_RESPONSE, len(stations),
				host_index, assigned_index, fragments, i,
				num_infos, offset
			])

			for j in range(num_infos):
				station_info = stations[offset + j]
				data += station_info.connection_info.serialize()
				data += bytes([station_info.index, 0])
			self.send(station, data, 0, True)
		
	def send_deny_join(self, station, reason):
		logger.info("Denying join request")
		data = bytes([self.MESSAGE_JOIN_RESPONSE, 0, 0xFF, 0xFF, reason])
		self.send(station, data, 0)
		self.send(station, data, 8)
		
	def send_destroy_response(self, station, station_index):
		logger.info("Sending destroy response")
		data = bytes([self.MESSAGE_DESTROY_RESPONSE, station_index])
		self.send(station, data, 0)
		self.send(station, data, 8)
		
	def send_update_mesh(self, counter, host_index, stations):
		logger.info("Sending mesh update")
		
		data = struct.pack(
			">BBBBIBBBB", self.MESSAGE_UPDATE_MESH, len(stations),
			host_index, 0, counter, 1, 0, host_index, 0
		)
		for station in stations:
			data += station.connection_info.serialize()
			data += bytes([station.index, 0])
			
		for reliable_transport in filter(None, self.sliding_windows):
			reliable_transport.send(data)
		
	def send(self, station, payload, flags, ack=False):
		message = PIAMessage()
		message.flags = flags
		message.protocol_id = self.PROTOCOL_ID
		message.protocol_port = self.PORT_UNRELIABLE
		message.payload = payload
		if ack:
			self.resender.send(station, message)
		else:
			self.transport.send(station, message)

			
class MeshMgr:
	
	mesh_created = signal.Signal()
	mesh_destroyed = signal.Signal()
	
	station_joined = signal.Signal()
	station_left = signal.Signal()
	
	JOIN_OK = 0
	JOIN_DENIED = 1
	JOIN_WAITING = 2
	JOIN_NONE = 3

	def __init__(self, session):
		self.session = session
		self.protocol = session.mesh_protocol
		self.protocol.on_join_request.add(self.handle_join_request)
		self.protocol.on_join_response.add(self.handle_join_response)
		self.protocol.on_join_denied.add(self.handle_join_denied)
		self.protocol.on_leave_request.add(self.handle_leave_request)
		self.protocol.on_leave_response.add(self.handle_leave_response)
		self.protocol.on_destroy_request.add(self.handle_destroy_request)
		self.protocol.on_destroy_response.add(self.handle_destroy_response)
		self.protocol.on_mesh_update.add(self.handle_mesh_update)
		
		self.station_mgr = session.station_mgr
		self.connection_mgr = session.connection_mgr
		
		self.stations = StationList()
		self.host_index = None
		
		self.update_counter = -1
		
		self.join_state = self.JOIN_NONE
		
	def is_host(self):
		return self.session.station.index == self.host_index
		
	def handle_join_request(self, station, station_index, station_addr):
		if self.is_host():
			if station != self.station_mgr.find_by_address(station_addr.address):
				logger.warning("Received join request with unexpected station address")
				self.protocol.send_deny_join(station, 2)
			else:
				logger.info("Received join request")
				index = self.stations.next_index()
				self.protocol.send_join_response(station, index, self.host_index, self.stations)
				self.stations.add(station)
				self.protocol.assign_sliding_window(station)
				self.send_update_mesh()
				self.station_joined(station)
		else:
			logger.warning("Received join request even though we aren't host")
			self.protocol.send_deny_join(station, 1)

	def handle_join_response(self, station, host_index, my_index, infos):
		if self.join_state != self.JOIN_WAITING:
			logger.warning("Unexpected join response received")
		else:
			host_index = infos[host_index].index
			my_index = infos[my_index].index
			logger.info("Received join response: (%i, %i)" %(host_index, my_index))
			self.join_state = self.JOIN_OK
			self.host_index = host_index
			self.stations.add(self.session.station, my_index)
			self.stations.add(station, host_index)
			self.protocol.assign_sliding_window(station)
			self.mesh_created(host_index, my_index)
			self.station_joined(station)
	
	def handle_join_denied(self, station, reason):
		logger.info("Join denied (%i)" %reason)
		self.join_state = self.JOIN_DENIED
		
	def handle_leave_request(self, station, station_index, station_address):
		if self.is_host():
			logger.warning("TODO: Handle leave request")
		else:
			logger.warning("Unexpected leave request received")
			
	def handle_leave_response(self, station, station_index, station_address):
		logger.warning("Unexpected leave response received")
		
	def handle_destroy_request(self, station, station_index, station_address):
		if self.is_host():
			logger.warning("Unexpected destroy request received")
		else:
			self.protocol.send_destroy_response(station, self.session.station.index)
			self.mesh_destroyed()
		
	def handle_destroy_response(self, station, station_index):
		logger.warning("Unexpected destroy response received")
		
	def handle_mesh_update(self, infos):
		disconnect_list = list(self.stations)
		connect_list = []
		for info in infos:
			station = self.station_mgr.find_by_connection_info(info.connection_info)
			if station in disconnect_list:
				disconnect_list.remove(station)
				if station.index != info.index:
					logger.error("Station index changed unexpectedly (%i -> %i)",
					             station.index, info.index)
			else:
				rvcid = info.connection_info.public_station.rvcid
				station = self.station_mgr.create(None, rvcid)
				self.stations.add(station, info.index)
				self.protocol.assign_sliding_window(station)
				if station.index < self.session.station.index:
					connect_list.append(info.connection_info)
					
		self.connection_mgr.connect(*connect_list)
		
	def handle_station_connected(self, station):
		if station.rvcid in self.pending_connect:
			index = self.pending_connect.pop(station.rvcid)
			if self.stations.is_usable(index):
				self.stations.add(station, index)
				self.protocol.assign_sliding_window(station)
				self.station_joined(station)
			else:
				logger.warning("Tried to assign station to occupied index")
		
	def send_update_mesh(self):
		self.update_counter += 1
		self.protocol.send_update_mesh(
			self.update_counter, self.host_index, self.stations
		)
	
	def create(self):
		self.stations.add(self.session.station)
		self.host_index = self.session.station.index
	
	def join(self, host_station):
		self.join_state = self.JOIN_WAITING
		self.protocol.send_join_request(host_station)
		while self.join_state == self.JOIN_WAITING:
			scheduler.update()
		if self.join_state == self.JOIN_DENIED:
			raise RuntimeError("Join request denied")
		
		logger.info("Wait until all stations are connected")
		all_connected = False
		while not all_connected:
			all_connected = True
			for station in self.stations:
				if not station.is_connected:
					all_connected = False
			scheduler.update()
		logger.info("Successfully joined a mesh!")
