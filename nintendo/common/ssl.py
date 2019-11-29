
from nintendo.common import socket, scheduler
from OpenSSL import SSL, crypto


TYPE_DER = 0
TYPE_PEM = 1

VERSION_SSL = 0
VERSION_TLS = 1
VERSION_TLS11 = 1
VERSION_TLS12 = 1

TypeMap = {
	TYPE_DER: crypto.FILETYPE_ASN1,
	TYPE_PEM: crypto.FILETYPE_PEM
}

VersionMap = {
	VERSION_SSL: SSL.SSLv3_METHOD,
	VERSION_TLS: SSL.TLSv1_METHOD,
	VERSION_TLS11: SSL.TLSv1_1_METHOD,
	VERSION_TLS12: SSL.TLSv1_2_METHOD
}


class SSLCertificate:
	def __init__(self, obj):
		self.obj = obj
		
	def public_key(self):
		pkey = self.obj.get_pubkey()
		rsakey = pkey.to_cryptography_key()
		return rsakey.public_numbers()
		
	@staticmethod
	def load(filename, format):
		with open(filename, "rb") as f:
			data = f.read()
		return SSLCertificate.parse(data, format)
		
	@staticmethod
	def parse(data, format):
		cert = crypto.load_certificate(TypeMap[format], data)
		return SSLCertificate(cert)
	
	
class SSLPrivateKey:
	def __init__(self, obj):
		self.obj = obj
		
	@staticmethod
	def load(filename, format):
		with open(filename, "rb") as f:
			data = f.read()
		return SSLPrivateKey.parse(data, format)
		
	@staticmethod
	def parse(data, format):
		pkey = crypto.load_privatekey(TypeMap[format], data)
		return SSLPrivateKey(pkey)


class SSLClient:
	def __init__(self, version=VERSION_TLS12, sock=None):
		self.s = sock
		if not self.s:
			self.s = socket.TCPClient()
		
		self.context = SSL.Context(VersionMap[version])
		
	def set_certificate(self, cert, key):
		self.context.use_certificate(cert.obj)
		self.context.use_privatekey(key.obj)
	
	def connect(self, host, port):
		sock = SSL.Connection(self.context, self.s.fd())
		sock.connect((host, port))
		sock.do_handshake()
		sock.setblocking(False)
		
		wrapper = socket.SocketWrapper(sock)
		self.s = socket.TCPClient(wrapper)
		return True
		
	def send(self, data): self.s.send(data)
	
	def recv(self, num=4096):
		try:
			return self.s.recv(num)
		except (SSL.ZeroReturnError, SSL.SysCallError):
			return b""
		except SSL.WantReadError:
			pass
	
	def close(self): self.s.close()
			
	def fd(self): return self.s.fd()
	def local_address(self): return self.s.local_address()
	def remote_address(self): return self.s.remote_address()


class SSLServer:
	def __init__(self, version=VERSION_TLS12, server=None):
		self.server = server
		if not self.server:
			self.server = socket.TCPServer()
		
		self.context = SSL.Context(VersionMap[version])
		
	def set_certificate(self, cert, key):
		self.context.use_certificate(cert.obj)
		self.context.use_privatekey(key.obj)
		
	def start(self, host, port):
		sock = SSL.Connection(self.context, self.server.fd())
		wrapper = socket.SocketWrapper(sock)
		self.server = socket.TCPServer(wrapper)
		self.server.start(host, port)
		
	def accept(self):
		client = self.server.accept()
		if client:
			return SSLClient(sock=client)
