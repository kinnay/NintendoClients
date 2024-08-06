
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from anynet import tls
import hashlib
import struct


def load_keys(filename):
	with open(filename) as f:
		lines = f.readlines()
	
	keys = {}
	for line in lines:
		line = line.strip()
		if line:
			name, key = line.split("=")
			keys[name.strip()] = bytes.fromhex(key)
	return keys


table = [
	0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
	0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400
]

def crc16(data):
	hash = 0x55AA
	for byte in data:
		r = table[hash & 0xF]
		hash = (hash >> 4) ^ r ^ table[byte & 0xF]
		
		r = table[hash & 0xF]
		hash = (hash >> 4) ^ r ^ table[byte >> 4]
	return hash


class ProdInfo:
	def __init__(self, keys, filename):
		self.keys = keys
		with open(filename, "rb") as f:
			self.data = f.read()
			
	def check(self, offset, size):
		end = offset + size - 2
		
		expected = struct.unpack_from("<H", self.data, end)[0]
		if crc16(self.data[offset : end]) != expected:
			raise ValueError("CRC16 check failed")
	
	def get_device_id(self):
		self.check(0x2A90, 0x250)
		return int(self.data[0x2B56:0x2B66], 16)
	
	def get_tls_cert(self):
		self.check(0xAD0, 0x10)
		
		length = struct.unpack_from("<I", self.data, 0xAD0)[0]
		if length > 0x800:
			raise ValueError("TLS certificate is too big")
			
		data = self.data[0xAE0 : 0xAE0 + length]
		hash = hashlib.sha256(data).digest()
		if hash != self.data[0x12E0 : 0x1300]:
			raise ValueError("SHA256 check failed")
		
		return tls.TLSCertificate.parse(data, tls.TYPE_DER)
		
	def get_tls_key(self):
		self.check(0x3AE0, 0x140)
		
		initial = self.data[0x3AE0 : 0x3AF0]
		cipher = self.data[0x3AF0 : 0x3BF0]
		
		kek = self.keys["ssl_rsa_kek_personalized"] if "ssl_rsa_kek_personalized" in self.keys else self.keys["ssl_rsa_kek"]
		aes = AES.new(kek, AES.MODE_CTR, nonce=b"", initial_value=initial)
		d = int.from_bytes(aes.decrypt(cipher), "big")
		
		pubkey = self.get_tls_cert().public_key()
		
		rsa = RSA.construct((pubkey.n, pubkey.e, d))
		der = rsa.export_key("DER")
		return tls.TLSPrivateKey.parse(der, tls.TYPE_DER)
