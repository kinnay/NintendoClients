
from nintendo.pia.packet import PIAMessage
from nintendo.nex.nat import NATTraversalClient
from nintendo.common import signal
import collections
import struct
import time

import logging
logger = logging.getLogger(__name__)


class NATProbeData(collections.namedtuple("NatProbeData", "connection_id probe_type system_time")):
	REQUEST = 0
	REPLY = 1
	
	fmt = ">IBxxxQ"
	
	@classmethod
	def deserialize(cls, data): return cls(*struct.unpack_from(cls.fmt, data))
	def serialize(self): return struct.pack(self.fmt, *self)
	
	@staticmethod
	def sizeof(): return 16


class NATTraversalProtocol:

	PROTOCOL_ID = 0x400
	
	PORT_PROBE_REQUEST = 1
	PORT_PROBE_REPLY = 2
	PORT_DUMMY = 3
	
	on_probe_request = signal.Signal()
	on_probe_reply = signal.Signal()

	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		
		self.handlers = {
			self.PORT_PROBE_REQUEST: self.handle_probe_request,
			self.PORT_PROBE_REPLY: self.handle_probe_reply
		}
		
	def handle(self, station, message):
		self.handlers[message.protocol_port](station, message.payload)
		
	def handle_probe_request(self, station, message):
		probe = NATProbeData.deserialize(message)
		self.on_probe_request(station, probe)
		
	def handle_probe_reply(self, station, message):
		probe = NATProbeData.deserialize(message)
		self.on_probe_reply(station, probe)
		
	def send_probe_request(self, station, count=1):
		logger.info("Sending NAT probe to %s", station.address)
		self.send_probe(station, NATProbeData.REQUEST, self.PORT_PROBE_REQUEST, count)
		
	def send_probe_reply(self, station, count=1):
		logger.info("Sending NAT probe reply to %s", station.address)
		self.send_probe(station, NATProbeData.REPLY, self.PORT_PROBE_REPLY, count)
		
	def send_probe(self, station, probe_type, protocol_port, count=1):
		for i in range(count):
			probe = NATProbeData(self.session.rvcid, probe_type, int(time.time()))
			message = PIAMessage()
			message.flags = 8
			message.protocol_id = self.PROTOCOL_ID
			message.protocol_port = protocol_port
			message.payload = probe.serialize()
			self.transport.send(station, message)

			
class NATTraversalMgr:

	nat_traversal_finished = signal.Signal()

	def __init__(self, session):
		self.backend = session.backend
	
		self.protocol = session.nat_protocol
		self.protocol.on_probe_request.add(self.handle_probe_request)
		self.protocol.on_probe_reply.add(self.handle_probe_reply)
		
		server = session.backend.nat_traversal_server
		server.handler.initiate_probe.add(self.handle_initiate_probe)
		self.client = NATTraversalClient(session.backend)
		
		self.station_mgr = session.station_mgr
		
		self.past_traversals = {}
		
	def init_station(self, url):
		station = self.station_mgr.find_by_rvcid(url["RVCID"])
		if station:
			station.address = url.get_address()
		else:
			station = self.station_mgr.create(url.get_address(), url["RVCID"])
		return station
	
	def handle_probe_request(self, station, probe):
		logger.info("Received probe request (%i, %i)", probe.connection_id, probe.system_time)
		self.protocol.send_probe_reply(station)
		
	def handle_probe_reply(self, station, probe):
		logger.info("Received probe reply: (%i, %i)", probe.connection_id, probe.system_time)
		self.past_traversals[station.rvcid] = time.monotonic()
		self.nat_traversal_finished(station)
		
	def handle_initiate_probe(self, source):
		logger.info("Received probe initiation request for %s" %source)
		if source["probeinit"] == 1:
			self.request_probe_initiation(source)
		station = self.init_station(source)
		self.protocol.send_probe_request(station, 3)
		
	def request_probe_initiation(self, target):
		logger.info("Sending probe initiation request to %s" %target)
		if target["type"] == 0:
			source = self.backend.local_station
		else:
			source = self.backend.public_station

		source = source.copy()
		if target["probeinit"] == 1:
			source["probeinit"] = 0
		else:
			source["probeinit"] = 1

		self.init_station(target)
		self.client.request_probe_initiation_ext([target], source)
		
	def report_nat_properties(self, props):
		logger.info("Reporting NAT properties")
		self.client.report_nat_properties(
			props.nat_mapping, props.nat_filtering, props.rtt
		)
		
	def start_nat_traversal(self, url):
		rvcid = url["RVCID"]
		if rvcid in self.past_traversals:
			if time.monotonic() - self.past_traversals[rvcid] < 30:
				station = self.station_mgr.find_by_rvcid(rvcid)
				self.nat_traversal_finished(station)
				return

		logger.info("Starting NAT traversal for %s" %url)
		target = url.copy()
		target["probeinit"] = 0
		self.request_probe_initiation(target)
