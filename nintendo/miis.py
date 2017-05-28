
from nintendo.common.stream import BitStreamIn

class MiiData:
	def __init__(self, data):
		#This struct probably contains tightly packed bit fields holding
		#enough information to generate a model of this mii, but when I
		#tried to parse it, I didn't get the results I was expecting
		stream = BitStreamIn(data)

		#FFLiMiiDataCore
		stream.seek(0x1A)
		self.mii_name = stream.wchars(10)
		
		#FFLiMiiDataOfficial
		
		#FFLStoreData
		stream.seek(0x5A)
		stream.u16() #CRC16 of this whole struct
