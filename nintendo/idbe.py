
from Crypto.Cipher import AES
from nintendo.common.streams import StreamIn
import requests
import hashlib


class IDBEStrings:
	def __init__(self, stream):
		self.short_name = stream.wchars(64).rstrip("\0")
		self.long_name = stream.wchars(128).rstrip("\0")
		self.publisher = stream.wchars(64).rstrip("\0")


class IDBEFile:
	def __init__(self, data):
		self.load(data)
		
	def is_wiiu(self, data):
		if len(data) == 0x36D0: return False
		if len(data) == 0x12080: return True
		raise ValueError("IDBE file has unexpected size")
		
	def load(self, data):
		sha = data[:32]
		if sha != hashlib.sha256(data[32:]).digest():
			raise ValueError("Incorrect SHA256 hash")
		
		wup = self.is_wiiu(data)
		
		endian = ">" if wup else "<"
		
		stream = StreamIn(data[32:], endian)
		
		self.title_id = stream.u64()
		self.title_version = stream.u32()
		self.unk1 = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.read(16)
		self.unk4 = stream.u32()
		self.unk5 = stream.u64()
		
		self.strings = []
		for i in range(16):
			self.strings.append(IDBEStrings(stream))
			
		if wup:
			self.tga = stream.read(0x1002C)
			self.unk6 = stream.u32()
		else:
			self.unk6 = stream.read(0x1680)


KEYS = [
	bytes.fromhex("4ab9a40e146975a84bb1b4f3ecefc47b"),
	bytes.fromhex("90a0bb1e0e864ae87d13a6a03d28c9b8"),
	bytes.fromhex("ffbb57c14e98ec6975b384fcf40786b5"),
	bytes.fromhex("80923799b41f36a6a75fb8b48c95f66f")
]

IV = bytes.fromhex("a46987ae47d82bb4fa8abc0450285fa4")


def get_platform(title_id):
	platform = title_id >> 48
	if platform == 4:
		return "ctr"
	elif platform == 5:
		return "wup"
	raise ValueError("Invalid title id")

def download(title_id, title_version=None):
	platform = get_platform(title_id)
	base_id = (title_id >> 8) & 0xFF
	
	url = "https://idbe-%s.cdn.nintendo.net/icondata/%02X/%016X" %(platform, base_id, title_id)
	if title_version is not None:
		url += "-%i" %title_version
	url += ".idbe"
	
	r = requests.get(url, verify=False)
	r.raise_for_status()
	return r.content
	
def check(data):
	if len(data) % 16 != 2: return False
	if data[0] != 0: return False
	if data[1] >= 4: return False
	return True

def decrypt(data):
	if not check(data):
		raise ValueError("IDBE data is invalid")
	
	index = data[1]
	key = KEYS[index]
	aes = AES.new(key, AES.MODE_CBC, IV)
	return aes.decrypt(data[2:])
