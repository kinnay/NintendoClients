
import struct
import socket

def ip_to_hex(ip):
	return struct.unpack(">I", socket.inet_aton(ip))[0]
