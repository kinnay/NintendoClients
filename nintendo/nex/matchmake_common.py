
from nintendo.nex import common


class Gathering(common.Structure):
	def __init__(self, id, owner_pid, host_pid, player_min, player_max, participation_policy, policy_argument, flags, state, description):
		self.id = id
		self.owner_pid = owner_pid
		self.host_pid = host_pid
		self.player_min = player_min
		self.player_max = player_max
		self.participation_policy = participation_policy
		self.policy_argument = policy_argument
		self.flags = flags
		self.state = state
		self.description = description
		
	def get_name(self):
		return "Gathering"
	
	def streamin(self, stream):
		stream.u32(self.id)
		stream.u32(self.owner_pid)
		stream.u32(self.host_pid)
		stream.u16(self.player_min)
		stream.u16(self.player_max)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.u32(self.flags)
		stream.u32(self.state)
		stream.string(self.description)
		
	def streamout(self, stream):
		self.id = stream.u32()
		self.owner_pid = stream.u32()
		self.host_pid = stream.u32()
		self.player_min = stream.u16()
		self.player_max = stream.u16()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.flags = stream.u32()
		self.state = stream.u32()
		self.description = stream.string()
common.DataHolder.register(Gathering, "Gathering")
