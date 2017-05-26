
from nintendo.nex.common import NexEncoder, DataHolder


class Gathering(NexEncoder):
	version_map = {
		30504: 0
	}
	
	def init(self, id, unk2, unk3, player_min, player_max, participation_policy, policy_argument, flags, unk4, description):
		self.id = id
		self.unk2 = unk2
		self.unk3 = unk3
		self.player_min = player_min
		self.player_max = player_max
		self.participation_policy = participation_policy
		self.policy_argument = policy_argument
		self.flags = flags
		self.unk4 = unk4
		self.description = description
		
	def get_name(self):
		return "Gathering"
	
	def encode_old(self, stream):
		stream.u32(self.id)
		stream.u32(self.unk2)
		stream.u32(self.unk3)
		stream.u16(self.player_min)
		stream.u16(self.player_max)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.u32(self.flags)
		stream.u32(self.unk4)
		stream.string(self.description)
		
	def decode_old(self, stream):
		self.id = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.player_min = stream.u16()
		self.player_max = stream.u16()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.flags = stream.u32()
		self.unk4 = stream.u32()
		self.description = stream.string()
		
	encode_v0 = encode_old
	decode_v0 = decode_old
DataHolder.register(Gathering, "Gathering")
