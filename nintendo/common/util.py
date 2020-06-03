
from nintendo.common.textstream import TextStream
import netifaces
import struct
import socket
import string

urlsafe = string.digits + string.ascii_letters + "~-_."

def ip_to_hex(ip):
	return struct.unpack(">I", socket.inet_aton(ip))[0]
	
def is_numeric(s):
	return all(c in string.digits for c in s)
	
def is_hexadecimal(s):
	return all(c in string.hexdigits for c in s)

def crc16(data):
	hash = 0
	for char in data:
		for i in range(8):
			flag = hash & 0x8000
			hash = (hash << 1) & 0xFFFF
			if flag:
				hash ^= 0x1021
				
		hash ^= char
	return hash
	
def local_address():
	interface = netifaces.gateways()["default"][netifaces.AF_INET][1]
	addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
	return addresses["addr"]
	
def broadcast_address():
	interface = netifaces.gateways()["default"][netifaces.AF_INET][1]
	addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
	return addresses["broadcast"]
	
def urlencode(s):
	out = ""
	for char in s:
		if char in urlsafe:
			out += char
		else:
			out += "%%%02X" %ord(char)
	return out
	
def urldecode(s):
	stream = TextStream(s)
	
	out = ""
	while not stream.eof():
		char = stream.read()
		if char == "%":
			if stream.available() >= 2 and is_hexadecimal(stream.peek(2)):
				out += chr(int(stream.read(2), 16))
			else:
				out += char
		else:
			out += char
	return out
			
