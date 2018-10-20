
from nintendo.pia.natcheck import NATDetecter
from nintendo.pia.nattraversal import NATTraversalProtocol, NATTraversalMgr
from nintendo.pia.station import StationLocation, StationConnectionInfo, \
	IdentificationInfo, StationProtocol, StationMgr
from nintendo.pia.mesh import MeshProtocol, MeshMgr
from nintendo.pia.keepalive import KeepAliveProtocol, KeepAliveMgr
from nintendo.pia.unreliable import UnreliableProtocol
from nintendo.pia.rtt import RttProtocol
from nintendo.pia.transport import MessageTransport, ResendingTransport
from nintendo.common import scheduler

import logging
logger = logging.getLogger(__name__)


class ConnectionMgr:

	RESULT_OK = 0
	RESULT_NONE = 1
	RESULT_TIMEOUT = 2
	RESULT_DENIED = 3

	def __init__(self, session):
		self.session = session
		self.backend = session.backend
		self.nat_mgr = session.nat_mgr
		self.nat_mgr.nat_traversal_finished.add(self.handle_nat_traversal_finished)
		self.station_mgr = session.station_mgr
		self.station_mgr.station_connected.add(self.handle_station_connected)
		self.station_mgr.station_disconnected.add(self.handle_station_disconnected)
		self.station_mgr.connection_denied.add(self.handle_connection_denied)
		
		self.timeouts = {}
		self.pending_nat = []
		self.pending_connect = []
		self.results = {}
	
	def connect(self, *infos):
		for info in infos:
			self.connect_async(info)
		for info in infos:
			self.wait(info)
		
	def connect_async(self, info):
		target_ip = info.public_station.address.address.host
		my_ip = self.backend.public_station["address"]
		
		target = info.public_station
		if target_ip == my_ip:
			target = info.local_station
	
		rvcid = target.rvcid
		if self.results.get(rvcid) != self.RESULT_OK:
			if rvcid == self.session.rvcid:
				self.results[rvcid] = self.RESULT_OK
			else:
				self.results[rvcid] = self.RESULT_NONE

				self.timeouts[rvcid] = scheduler.add_timeout(
					self.handle_timeout, 8, False, rvcid
				)
				
				self.pending_nat.append(rvcid)
				self.nat_mgr.start_nat_traversal(target.to_station_url())
		
	def wait(self, info):
		rvcid = info.public_station.rvcid
		while self.results[rvcid] == self.RESULT_NONE:
			scheduler.update()
			
		result = self.results[rvcid]
		if result == self.RESULT_TIMEOUT:
			raise ConnectionError("Connection timed out")
		if result == self.RESULT_DENIED:
			raise ConnectionError("Connection denied")
		
	def handle_nat_traversal_finished(self, station):
		if station.rvcid in self.pending_nat:
			logger.info("NAT traversal completed")
			self.pending_connect.append(station.rvcid)
			self.pending_nat.remove(station.rvcid)
			self.station_mgr.connect(station)
			
	def handle_station_connected(self, station):
		if station.rvcid in self.pending_connect:
			logger.info("Successfully connected to station")
			self.pending_connect.remove(station.rvcid)
			self.results[station.rvcid] = self.RESULT_OK
			scheduler.remove(self.timeouts.pop(station.rvcid))
			
	def handle_connection_denied(self, station):
		if station.rvcid in self.pending_connect:
			self.results[station.rvcid] = self.RESULT_DENIED
			scheduler.remove(self.timeouts.pop(station.rvcid))
			self.pending_connect.remove(station.rvcid)
			
	def handle_timeout(self, rvcid):
		logger.warning("Connection attempt timed out (rvcid=%i)", rvcid)
		self.timeouts.pop(rvcid)
		if rvcid in self.pending_nat:
			self.pending_nat.remove(rvcid)
		if rvcid in self.pending_connect:
			self.pending_connect.remove(rvcid)

			station = self.station_mgr.find_by_rvcid(rvcid)
			self.station_mgr.cancel_connection(station)
		self.results[rvcid] = self.RESULT_TIMEOUT

	def handle_station_disconnected(self, station):
		if self.results.get(station.rvcid) == self.RESULT_OK:
			del self.results[station.rvcid]
		
		
class PIASession:
	def __init__(self, backend, session_key):
		self.backend = backend
		self.session_key = session_key
		
		self.transport = MessageTransport(self)
		self.resending_transport = ResendingTransport(self.transport)
		
		self.nat_protocol = NATTraversalProtocol(self)
		self.station_protocol = StationProtocol(self)
		self.mesh_protocol = MeshProtocol(self)
		self.keep_alive_protocol = KeepAliveProtocol(self)
		self.unreliable_protocol = UnreliableProtocol(self)
		self.rtt_protocol = RttProtocol(self)
		
		self.protocols = {
			NATTraversalProtocol.PROTOCOL_ID: self.nat_protocol,
			StationProtocol.PROTOCOL_ID: self.station_protocol,
			MeshProtocol.PROTOCOL_ID: self.mesh_protocol,
			KeepAliveProtocol.PROTOCOL_ID: self.keep_alive_protocol,
			UnreliableProtocol.PROTOCOL_ID: self.unreliable_protocol,
			RttProtocol.PROTOCOL_ID: self.rtt_protocol
		}
		
		self.station_mgr = StationMgr(self)
		self.nat_mgr = NATTraversalMgr(self)
		self.connection_mgr = ConnectionMgr(self)
		self.mesh_mgr = MeshMgr(self)
		self.keep_alive_mgr = KeepAliveMgr(self)
		
	def start(self, identification, name):
		logger.info("Initializing PIA session")
		
		#Rendez-Vous connection id
		self.rvcid = self.backend.local_station["RVCID"]
	
		detecter = NATDetecter()
		props = detecter.get_nat_properties()
		self.nat_mgr.report_nat_properties(props)

		self.create_local_station(props, identification, name)
		
		self.transport.start(props.local_address)
		self.transport.packet_received.add(self.handle_packet)
		
	def close(self):
		logger.info("Closing PIA session")
		print("TODO: Implement PIASession.close")
			
	def create_local_station(self, props, identification, name):
		self.station = self.station_mgr.create(props.local_address, self.rvcid)
		self.station.is_connected = True
	
		local_station_url = self.backend.local_station.copy()
		local_station_url["natm"] = props.nat_mapping
		local_station_url["natf"] = props.nat_filtering
		local_station_url["port"] = props.local_address[1]
		
		public_station_url = self.backend.public_station.copy()
		public_station_url["natm"] = props.nat_mapping
		public_station_url["natf"] = props.nat_filtering
		public_station_url["port"] = props.public_address[1]
		
		self.backend.secure_client.replace_url(self.backend.local_station, local_station_url)
		self.backend.local_station = local_station_url
		self.backend.public_station = public_station_url
		
		local_location = StationLocation.from_station_url(local_station_url)
		public_location = StationLocation.from_station_url(public_station_url)
		self.station.connection_info = StationConnectionInfo(public_location, local_location)
		
		self.station.identification_info = IdentificationInfo(identification, name)
		
	def create_mesh(self):
		self.mesh_mgr.create()
		
	def join_mesh(self, host_urls):
		station = self.connect_to_host(host_urls)
		self.mesh_mgr.join(station)
		
	def connect_to_host(self, host_urls):
		public_url = None
		local_url = None
		
		for url in host_urls:
			if url.is_public():
				public_url = url
			else:
				local_url = url
				
		if not public_url or not local_url:
			raise ValueError("Incomplete station url list")
			
		public_location = StationLocation.from_station_url(public_url)
		local_location = StationLocation.from_station_url(local_url)
		conn_info = StationConnectionInfo(public_location, local_location)
		
		self.connection_mgr.connect(conn_info)
		return self.station_mgr.find_by_rvcid(public_url["RVCID"])
		
	def handle_packet(self, station, packet):
		protocol_id = packet.protocol_id
		if protocol_id in self.protocols:
			self.protocols[protocol_id].handle(station, packet)
		else:
			logger.warning("Unknown protocol id: 0x%X" %protocol_id)
