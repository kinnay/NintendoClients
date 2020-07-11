
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from nintendo.common import ssl
import hashlib
import struct
import base64

import logging
logger = logging.getLogger(__name__)


class HTTPError(Exception):
	def __init__(self, *, status_code=None, errors=None):
		self.status_code = status_code
		self.errors = errors

	def __str__(self):
		if self.errors is not None:
			return errors[0]["message"]
		return "HTTP request failed with status code: %i" %self.status_code


def b64encode(data):
	return base64.b64encode(data, b"-_").decode().rstrip("=")
	
def b64decode(text):
	length = (len(text) + 3) & ~3
	text = text.ljust(length, "=")
	return base64.b64decode(text.encode(), b"-_")


class KeySet:
	def __init__(self, filename):
		self.keys = {}
		
		with open(filename) as f:
			lines = f.readlines()
			
		for line in lines:
			line = line.strip()
			if line:
				name, key = line.split("=")
				self.keys[name.strip()] = bytes.fromhex(key)
	
	def get(self, name):
		return self.keys[name]


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
	def __init__(self, keyset, filename):
		self.keyset = keyset
		with open(filename, "rb") as f:
			self.data = f.read()
			
	def check(self, offset, size):
		end = offset + size - 2
		
		expected = struct.unpack_from("<H", self.data, end)[0]
		if crc16(self.data[offset : end]) != expected:
			raise ValueError("CRC16 check failed")
			
	def get_platform_region(self):
		self.check(0x3510, 0x10)
		region_code = struct.unpack_from("<I", self.data, 0x3510)[0]
		return 2 if region_code == 4 else 1
	
	def get_ssl_cert(self):
		self.check(0xAD0, 0x10)
		
		length = struct.unpack_from("<I", self.data, 0xAD0)[0]
		if length > 0x800:
			raise ValueError("SSL certificate is too big")
			
		data = self.data[0xAE0 : 0xAE0 + length]
		hash = hashlib.sha256(data).digest()
		if hash != self.data[0x12E0 : 0x1300]:
			raise ValueError("SHA256 check failed")
		
		return ssl.SSLCertificate.parse(data, ssl.TYPE_DER)
		
	def get_ssl_key(self):
		self.check(0x3AE0, 0x140)
		
		initial = self.data[0x3AE0 : 0x3AF0]
		cipher = self.data[0x3AF0 : 0x3BF0]
		
		kek = self.keyset.get("ssl_rsa_kek")
		aes = AES.new(kek, AES.MODE_CTR, nonce=b"", initial_value=initial)
		d = int.from_bytes(aes.decrypt(cipher), "big")
		
		pubkey = self.get_ssl_cert().public_key()
		
		rsa = RSA.construct((pubkey.n, pubkey.e, d))
		der = rsa.export_key("DER")
		return ssl.SSLPrivateKey.parse(der, ssl.TYPE_DER)


class TicketList:
	def __init__(self, list_file, ticket_file):
		with open(list_file, "rb") as f:
			list_data = f.read()
			
		with open(ticket_file, "rb") as f:
			ticket_data = f.read()
			
		self.tickets = {}
		for i in range(len(list_data) // 0x20):
			rights_id = list_data[i * 0x20 : i * 0x20 + 0x10]
			title_id, key_revision = struct.unpack(">qq", rights_id)
			if title_id == -1 and key_revision == -1:
				break
			
			ticket_id = struct.unpack_from("<q", list_data, i * 0x20 + 16)[0]
			
			ticket_chunk = ticket_data[i * 0x400 : (i + 1) * 0x400]
			signature_type = struct.unpack_from("<I", ticket_chunk)[0]
			if signature_type != 0x010004:
				raise ValueError("Invalid signature type: 0x%X" %signature_type)
			
			ticket_size = 0x2C0 + struct.unpack_from("<I", ticket_chunk, 0x2B4)[0]
			if ticket_size > 0x400:
				raise ValueError("Found ticket with invalid size")
				
			if ticket_id != struct.unpack_from("<q", ticket_chunk, 0x290)[0]:
				raise ValueError("Ticket has unexpected ticket id")
				
			if rights_id != ticket_chunk[0x2A0 : 0x2B0]:
				raise ValueError("Ticket has unexpected rights id")
			
			ticket = ticket_chunk[:ticket_size]
			
			if title_id in self.tickets:
				logger.warning("Found multiple tickets for title %016X" %title_id)
			self.tickets[title_id] = ticket
			
	def get(self, title_id):
		if title_id not in self.tickets:
			raise ValueError("No ticket found for %016X" %title_id)
		return self.tickets[title_id]
