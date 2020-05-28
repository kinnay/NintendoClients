
from nintendo.common import socket, scheduler
from OpenSSL import crypto
import tempfile
import ssl

import logging
logger = logging.getLogger(__name__)


TYPE_DER = 0
TYPE_PEM = 1

VERSION_TLS = 0
VERSION_TLS11 = 1
VERSION_TLS12 = 2

TypeMap = {
	TYPE_DER: crypto.FILETYPE_ASN1,
	TYPE_PEM: crypto.FILETYPE_PEM
}

VersionMap = {
	VERSION_TLS: ssl.PROTOCOL_TLS,
	VERSION_TLS11: ssl.PROTOCOL_TLSv1_1,
	VERSION_TLS12: ssl.PROTOCOL_TLSv1_2
}


class SSLCertificate:
	def __init__(self, obj):
		self.obj = obj
		
	def public_key(self):
		pkey = self.obj.get_pubkey()
		rsakey = pkey.to_cryptography_key()
		return rsakey.public_numbers()
		
	def encode(self, format):
		return crypto.dump_certificate(TypeMap[format], self.obj)
		
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
		
		subject = cert.get_subject()
		subject.commonName = "*"
		
		cert.sign(key.obj, "sha1")
		
		return SSLCertificate(cert)
	
	
class SSLPrivateKey:
	def __init__(self, obj):
		self.obj = obj
		
	def encode(self, format):
		return crypto.dump_privatekey(TypeMap[format], self.obj)
		
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


class SSLContext:
	def __init__(self, version):
		self.context = ssl.SSLContext(VersionMap[version])
		
	def set_certificate(self, cert, key):
		certfile = tempfile.NamedTemporaryFile()
		keyfile = tempfile.NamedTemporaryFile()
		
		certfile.write(cert.encode(TYPE_PEM))
		keyfile.write(key.encode(TYPE_PEM))
		
		certfile.flush()
		keyfile.flush()
		
		self.context.load_cert_chain(certfile.name, keyfile.name)
		
		certfile.close()
		keyfile.close()
		
	def wrap(self, sock, host=None):
		if host is None:
			return self.context.wrap_socket(sock, True)
		return self.context.wrap_socket(sock, False, server_hostname=host)


class SSLClient:
	def __init__(self, version=VERSION_TLS12, sock=None):
		self.s = sock
		if not self.s:
			self.s = socket.TCPClient()
		
		self.context = SSLContext(version)
		
	def set_certificate(self, cert, key):
		self.context.set_certificate(cert, key)
	
	def connect(self, host, port, timeout=3):
		sock = self.context.wrap(self.s.fd(), host)
		wrapper = socket.SocketWrapper(sock)
		self.s = socket.TCPClient(wrapper)
		return self.s.connect(host, port, timeout)
		
	def send(self, data):
		self.s.send(data)
	
	def recv(self, num=4096):
		return self.s.recv(num)
	
	def close(self):
		self.s.close()
			
	def remote_certificate(self):
		cert = self.fd().getpeercert(True)
		if cert:
			return SSLCertificate.parse(cert, TYPE_DER)
			
	def fd(self): return self.s.fd()
	def local_address(self): return self.s.local_address()
	def remote_address(self): return self.s.remote_address()


class SSLServer:
	def __init__(self, version=VERSION_TLS12, server=None):
		self.server = server
		if not self.server:
			self.server = socket.TCPServer()
		
		key = SSLPrivateKey.generate()
		cert = SSLCertificate.generate(key)
		self.context = SSLContext(version)
		self.context.set_certificate(cert, key)
		
	def set_certificate(self, cert, key):
		self.context.set_certificate(cert, key)
		
	def start(self, host, port):
		sock = self.context.wrap(self.server.fd())
		wrapper = socket.SocketWrapper(sock)
		self.server = socket.TCPServer(wrapper)
		self.server.start(host, port)
		
	def accept(self):
		client = self.server.accept()
		if client:
			return SSLClient(sock=client)
