
class JoinState:
	NONE = 0
	JOINING = 1
	WAIT_CONNECTIONS = 2
	JOINED = 3
	ERROR = 4


class Mesh:
	def __init__(self):
		self.stations = [None] * 32
		
		self.host_index = None
		
		self.join_state = JoinState.NONE
		
	def get_stations(self):
		return [s for s in self.stations if s]
		
	def create(self, host):
		self.add_station(host)
		self.host_index = host.index
		
		self.join_state = JoinState.JOINED
		
	def find_free_index(self):
		for i in range(32):
			if self.stations[i] is None:
				return i
		raise RuntimeError("Mesh is full")
		
	def add_station(self, station, index=None):
		if index is None:
			index = self.find_free_index()
		if self.stations[index] is not None:
			raise ValueError("Station index is occupied")
		self.stations[index] = station
		station.index = index
		
	def set_host_index(self, index):
		self.host_index = index
	
	def get_host_index(self):
		return self.host_index
		
	def get_num_participants(self):
		participants = 0
		for station in self.stations:
			participants += station.identification_info.participants
		return participants
