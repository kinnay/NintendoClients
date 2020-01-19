
from nintendo.pia.types import StationConnectionInfo, IdentificationInfo
from nintendo.common import scheduler
import random
import time


class ConnectionState:
	DISCONNECTED = 0
	WAIT_INVERSE_REQUEST = 1
	WAIT_INVERSE_RESPONSE = 2
	WAIT_RESPONSE = 3
	CONNECTED = 4
	ERROR = 5


class Station:
	def __init__(self):
		self.session_start = time.monotonic()
		
		self.address = None
		
		self.rtt_timer = None
		self.base_timer = None
		
		self.index = 0xFD
		self.id = None
		
		self.connection_state = ConnectionState.DISCONNECTED
		
		self.connection_id_out_temp = 0
		self.connection_id_in_temp = 0
		self.connection_id_out = 0
		self.connection_id_in = 0
		self.sequence_id_out = 0
		self.sequence_id_in = 1
		
		self.nonce = 0
		
		self.connection_info = StationConnectionInfo()
		self.identification_info = None
		
	def is_connected(self):
		return self.connection_state == ConnectionState.CONNECTED
		
	def wait_connected(self, timeout=3):
		start = time.monotonic()
		while self.connection_state != ConnectionState.CONNECTED:
			if time.monotonic() - start > timeout:
				raise RuntimeError("Station connection timed out")
			if self.connection_state == ConnectionState.ERROR:
				raise RuntimeError("Station connection failed")
			scheduler.update()
		
	def next_sequence_id(self):
		if self.is_connected():
			self.sequence_id_out += 1
			if self.sequence_id_out == 0x10000:
				self.sequence_id_out = 1
		return self.sequence_id_out
		
	def set_address(self, addr): self.address = addr


class StationTable:
	def __init__(self):
		self.stations = []
		
	def __iter__(self):
		return iter(self.stations)
		
	def create(self):
		station = Station()
		self.stations.append(station)
		return station
		
	def find_by_address(self, address, create=False):
		for station in self.stations:
			if station.address == address:
				return station
				
		if create:
			station = self.create()
			station.set_address(address)
			return station
			
	def find_by_index(self, index):
		for station in self.stations:
			if station.index == index:
				return station

