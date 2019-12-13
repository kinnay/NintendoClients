
from nintendo.common import socket, scheduler
from OpenSSL import SSL, crypto

import logging
logger = logging.getLogger(__name__)


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
		
	@staticmethod
	def generate(key):
		cert = crypto.X509()
		cert.set_pubkey(key.obj)
		
		cert.set_notBefore(b"20000101000000Z")
		cert.set_notAfter(b"29990101000000Z")
		
		cert.sign(key.obj, "sha1")
		
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
		
	@staticmethod
	def generate():
		pkey = crypto.PKey()
		pkey.generate_key(crypto.TYPE_RSA, 1024)
		return SSLPrivateKey(pkey)


# Using PyOpenSSL here because Python's own ssl
# library doesn't support loading certificates
# from memory. PyOpenSSL has weird behavior in
# non-blocking mode though :(
class SSLClient:
	def __init__(self, version=VERSION_TLS12, sock=None):
		if not sock:
			sock = socket.TCPClient()
		self.remote_addr = sock.remote_address()
		self.s = sock.fd()
		
		self.context = SSL.Context(VersionMap[version])
		
	def set_certificate(self, cert, key):
		self.context.use_certificate(cert.obj)
		self.context.use_privatekey(key.obj)
	
	def connect(self, host, port):
		self.s = SSL.Connection(self.context, self.s)
		self.s.set_tlsext_host_name(host.encode())
		self.s.connect((host, port))
		self.s.setblocking(False)
		return True
		
	def send(self, data):
		while data:
			try:
				length = self.s.send(data)
				data = data[length:]
			except SSL.WantReadError:
				pass
			except SSL.SysCallError as e:
				if e.args[0] == 11: #EAGAIN
					pass
				else:
					raise
	
	def recv(self, num=4096):
		try:
			return self.s.recv(num)
		except SSL.WantReadError:
			pass
		except SSL.ZeroReturnError:
			logger.debug("Socket was closed")
			return b""
		except SSL.SysCallError as e:
			if e.args[0] == -1:
				logger.debug("Socket was closed unexpectedly")
				return b""
			else:
				raise e
		except SSL.Error as e:
			for error in e.args[0]:
				logger.error("An SSL error occurred: %s" %error[2])
			self.s.close()
			return b""
	
	def close(self):
		self.s.shutdown()
		self.s.close()
			
	def fd(self): return self.s
	def local_address(self): return self.s.getsockname()
	def remote_address(self): return self.remote_addr


class SSLServer:
	def __init__(self, version=VERSION_TLS12, server=None):
		self.server = server
		if not self.server:
			self.server = socket.TCPServer()
		
		self.version = VersionMap[version]
		
		key = SSLPrivateKey.generate()
		cert = SSLCertificate.generate(key)
		self.context = SSL.Context(self.version)
		self.context.use_certificate(cert.obj)
		self.context.use_privatekey(key.obj)
		
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
