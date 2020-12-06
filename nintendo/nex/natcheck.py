
from anynet import util
import struct


PRIMARY_ADDRESS = "nncs1-lp1.n.n.srv.nintendo.net"
PRIMARY_PORT = 10025


async def detect_external_address(socket):
	message = struct.pack(">IIII", 1, 0, 0, 0)
	await socket.send(message, (PRIMARY_ADDRESS, PRIMARY_PORT))
	
	while True:
		response = (await socket.recv())[0]
		if len(response) == 16:
			type, port, host, extra = struct.unpack(">IIII", response)
			if type == 1:
				return util.ip_from_hex(host), port
