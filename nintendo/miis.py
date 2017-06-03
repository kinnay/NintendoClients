
from nintendo.common.stream import BitStreamIn, BitStreamOut
from nintendo.common import util

class MiiData:
	#This struct probably contains tightly packed bit fields holding
	#enough information to generate a model of this mii, but when I
	#tried to parse it, I didn't get the results I was expecting

	#For some reason, mii name chars seem to be little endian,
	#while the CRC16 checksum is big endian
	
	def decode(self, stream):
		#FFLiMiiDataCore
		self.chunk1 = stream.read(0x1A)
		self.mii_name = stream.wchars(10).strip("\x00")
		self.chunk2 = stream.read(0x1A)
		
		#FFLiMiiDataOfficial
		self.chunk3 = stream.read(0x14)
		
		#FFLStoreData
		self.chunk4 = stream.read(2)
		stream.u16() #CRC16 of this whole struct
		
	def encode(self, stream):
		#FFLiMiiDataCore
		stream.write(self.chunk1)
		stream.wchars(self.mii_name + "\x00" * (10 - len(self.mii_name)))
		stream.write(self.chunk2)
		
		#FFLiMiiDataOfficial
		stream.write(self.chunk3)
		
		#FFLStoreData
		stream.write(self.chunk4)

		stream.endian = ">"
		stream.u16(util.crc16(stream.buffer))
		
	def build(self):
		stream = BitStreamOut()
		self.encode(stream)
		return stream.buffer
	
	@classmethod
	def parse(cls, data):
		instance = cls()
		instance.decode(BitStreamIn(data))
		return instance
