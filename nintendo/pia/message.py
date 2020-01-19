
from nintendo.pia.packet import PacketTransport, PIAPacket
from nintendo.pia.streams import StreamIn, StreamOut
from nintendo.common import scheduler
import zlib


class PIAMessage:
	def __init__(self):
		self.flags = 0
		self.station_index = 0xFD
		self.destination = 0
		self.station_id = 0
		self.protocol_id = 0
		self.protocol_port = 0
		self.payload_size = 0
		self.payload = b""
		
	def copy(self):
		message = PIAMessage()
		message.flags = self.flags
		message.station_index = self.station_index
		message.destination = self.destination
		message.station_id = self.station_id
		message.protocol_id = self.protocol_id
		message.protocol_port = self.protocol_port
		message.payload_size = self.payload_size
		message.payload = self.payload
		return message
		
		
class MessageEncoderV0:
	def decode(self, stream, message):
		message.flags = stream.u8()
		message.station_index = stream.u8()
		message.payload_size = stream.u16()
		message.destination = stream.u32()
		message.station_id = stream.u32()
		message.protocol_id = stream.u16()
		message.protocol_port = stream.u16()
		
		if stream.u32() != 0:
			logger.error("Reserved field should be cleared")
			return False
			
		message.payload = stream.read(message.payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream, message):
		stream.u8(message.flags)
		stream.u8(message.station_index)
		stream.u16(len(message.payload))
		stream.u32(message.destination)
		stream.u32(message.station_id)
		stream.u16(message.protocol_id)
		stream.u16(message.protocol_port)
		stream.u32(0) #Reserved
		
		stream.write(message.payload)
		stream.align(4)
		
		
class MessageEncoderV1:
	def decode(self, stream, message):
		message.flags = stream.u8()
		message.payload_size = stream.u16()
		message.destination = stream.u64()
		message.station_id = stream.u64()
		message.protocol_id = stream.u8()
		message.protocol_port = stream.u8()
		
		if stream.read(3) != bytes(3):
			logger.error("Padding bytes should be zero")
			return False
			
		message.payload = stream.read(message.payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream, message):
		stream.u8(message.flags)
		stream.u16(len(message.payload))
		stream.u64(message.destination)
		stream.u64(message.station_id)
		stream.u8(message.protocol_id)
		stream.u8(message.protocol_port)
		stream.pad(3)
		
		stream.write(message.payload)
		stream.align(4)
		
		
class MessageEncoderV2:
	def decode(self, stream, message):
		message.flags = stream.u8()
		
		if stream.u8() != 1:
			logger.error("Unexpected version number in message header")
			return False
			
		message.payload_size = stream.u16()
		message.protocol_id = stream.u8()
		message.protocol_port = stream.u8()
		message.destination = stream.u64()
		message.station_id = stream.u64()
			
		message.payload = stream.read(message.payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream, message):
		stream.u8(message.flags)
		stream.u8(1)
		stream.u16(len(message.payload))
		stream.u8(message.protocol_id)
		stream.u8(message.protocol_port)
		stream.u64(message.destination)
		stream.u64(message.station_id)
		
		stream.write(message.payload)
		stream.align(4)
		
		
class MessageEncoderV3:
	def decode(self, stream, message):
		message.flags = stream.u8()
		
		if stream.u8() != 2:
			logger.error("Unexpected version number in message header")
			return False
			
		message.payload_size = stream.u16()
		message.protocol_id = stream.u8()
		message.protocol_port = stream.u24()
		message.destination = stream.u64()
		message.station_id = stream.u64()
			
		message.payload = stream.read(message.payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream, message):
		stream.u8(message.flags)
		stream.u8(2)
		stream.u16(len(message.payload))
		stream.u8(message.protocol_id)
		stream.u24(message.protocol_port)
		stream.u64(message.destination)
		stream.u64(message.station_id)
		
		stream.write(message.payload)
		stream.align(4)
		
		
class MessageEncoderV4:
	def decode(self, stream, message):
		flags = stream.u8()
	
		if flags & 1:
			message.flags = stream.u8()
		
		if flags & 2:
			message.payload_size = stream.u16()
			
		if flags & 4:
			message.protocol_id = stream.u8()
			message.protocol_port = stream.u24()
			
		if flags & 8:
			message.destination = stream.u64()
		
		if flags & 16:
			message.station_id = stream.u64()
			
		message.payload = stream.read(message.payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream, message):
		stream.u8(0x7F)
		stream.u8(message.flags)
		stream.u16(len(message.payload))
		stream.u8(message.protocol_id)
		stream.u24(message.protocol_port)
		stream.u64(message.destination)
		stream.u64(message.station_id)
		
		stream.write(message.payload)
		stream.align(4)
		
		
MessageEncoders = [
	MessageEncoderV0,
	MessageEncoderV1,
	MessageEncoderV2,
	MessageEncoderV3,
	MessageEncoderV4
]
		
		
class MessageTransport:
	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		
		self.transport = PacketTransport(session)
		
		self.event = None
		
		self.messages = []
		
	def local_address(self): return self.transport.local_address()
		
	def prepare(self):
		version = self.settings.get("pia.message_version")
		self.encoder = MessageEncoders[version]()
		
		self.transport.prepare()
		self.event = scheduler.add_socket(self.handle_recv, self.transport)
		
	def cleanup(self):
		scheduler.remove(self.event)
		self.transport.cleanup()
		
	def send(self, station, message):
		message.flags = 1
		
		message.destination = 0
		if station.index != 0xFD:
			message.destination = 1 << station.index
			
		local_station = self.session.local_station()
		message.station_index = local_station.index
		message.station_id = local_station.id
		
		stream = StreamOut(self.settings)
		self.encoder.encode(stream, message)
		
		packet = PIAPacket(self.session)
		packet.payload = stream.get()
		self.transport.send(station, packet)
		
	def broadcast(self, port, message):
		message.flags = 1
		
		stream = StreamOut(self.settings)
		self.encoder.encode(stream, message)
		
		packet = PIAPacket(self.session)
		packet.payload = stream.get()
		self.transport.broadcast(port, packet)
		
	def handle_recv(self, pair):
		station, packet = pair
		
		message = PIAMessage()
		
		stream = StreamIn(packet.payload, self.settings)
		while not stream.eof():
			peek = stream.peek(stream.available())
			if all(x == 0xFF for x in peek):
				break
			
			message = message.copy()
			if not self.encoder.decode(stream, message):
				return
			
			if message.flags & 0x10:
				message.payload = zlib.decompress(message.payload)
			
			if station.id is None:
				station.id = message.station_id
			elif station.id != message.station_id:
				logger.error("Received message with wrong station id")
				return
			
			self.messages.append((station, message))
			
	def recv(self):
		if self.messages:
			return self.messages.pop(0)
