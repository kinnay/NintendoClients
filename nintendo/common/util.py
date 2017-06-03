
import struct
import socket

def ip_to_hex(ip):
	return struct.unpack(">I", socket.inet_aton(ip))[0]

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
