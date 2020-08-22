
from nintendo.common import socketutils, util
from OpenSSL import crypto
import contextlib
import tempfile
import anyio
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


class X509Name:
	ITEMS = {
		"C": "country_name",
		"ST": "state_or_province_name",
		"L": "locality_name",
		"O": "organization_name",
		"OU": "organizational_unit_name",
		"CN": "common_name",
		"E": "email_address"
	}
	
	ATTRS = {
		"country_name": "countryName",
		"state_or_province_name": "stateOrProvinceName",
		"locality_name": "localityName",
		"organization_name": "organizationName",
		"organizational_unit_name": "organizationalUnitName",
		"common_name": "commonName",
		"email_address": "emailAddress"
	}
	
	def __init__(self):
		# Why can't we create an X509Name directly?
		self.obj = crypto.X509().get_subject()
	
	def __getitem__(self, key):
		return getattr(self, self.ITEMS[key])
	def __setitem__(self, key, value):
		setattr(self, self.ITEMS[key], value)
		
	def __getattr__(self, name):
		return getattr(self.__dict__["obj"], X509Name.ATTRS[name])
	def __setattr__(self, name, value):
		if name == "obj":
			self.__dict__["obj"] = value
		else:
			setattr(self.obj, X509Name.ATTRS[name], value)


class TLSCertificate:
	def __init__(self, obj):
		self.obj = obj
		self.subject = X509Name()
		self.subject.obj = obj.get_subject()
		self.issuer = X509Name()
		self.issuer.obj = obj.get_issuer()
		
	def public_key(self):
		pkey = self.obj.get_pubkey()
		rsakey = pkey.to_cryptography_key()
		return rsakey.public_numbers()
		
	def encode(self, format):
		return crypto.dump_certificate(TypeMap[format], self.obj)
		
	def save(self, filename, format):
		with open(filename, "wb") as f:
			f.write(self.encode(format))
		
	def sign(self, key, alg="sha256"):
		self.obj.sign(key.obj, alg)
	
	@classmethod
	def load(cls, filename, format):
		with open(filename, "rb") as f:
			data = f.read()
		return cls.parse(data, format)
		
	@classmethod
	def parse(cls, data, format):
		cert = crypto.load_certificate(TypeMap[format], data)
		return cls(cert)
		
	@classmethod
	def generate(cls, key):
		cert = crypto.X509()
		cert.set_pubkey(key.obj)
		
		cert.set_notBefore(b"20000101000000Z")
		cert.set_notAfter(b"29990101000000Z")
		
		return cls(cert)
	
	
class TLSPrivateKey:
	def __init__(self, obj):
		self.obj = obj
		
	def encode(self, format):
		return crypto.dump_privatekey(TypeMap[format], self.obj)
	
	def save(self, filename, format):
		with open(filename, "wb") as f:
			f.write(self.encode(format))
	
	@classmethod
	def load(cls, filename, format):
		with open(filename, "rb") as f:
			data = f.read()
		return cls.parse(data, format)
		
	@classmethod
	def parse(cls, data, format):
		pkey = crypto.load_privatekey(TypeMap[format], data)
		return cls(pkey)
		
	@classmethod
	def generate(cls):
		pkey = crypto.PKey()
		pkey.generate_key(crypto.TYPE_RSA, 1024)
		return cls(pkey)


class TLSContext:
	def __init__(self, version=VERSION_TLS):
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
		
	def set_authority(self, authority):
		data = authority.encode(TYPE_DER)
		self.context.load_verify_locations(cadata=data)
		self.context.verify_mode = ssl.CERT_REQUIRED
		
	def load_default_authorities(self):
		self.context.load_default_certs()
		self.context.verify_mode = ssl.CERT_REQUIRED
	
	def get(self, server):
		if not server and self.context.verify_mode == ssl.CERT_REQUIRED:
			self.context.check_hostname = True
		else:
			self.context.check_hostname = False
		return self.context


class TLSClient:
	def __init__(self, stream):
		self.stream = stream
		
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		await self.close()
		
	async def send(self, data):
		await self.stream.send_all(data)
	
	async def recv(self, num=65536):
		data = await self.stream.receive_some(num)
		if not data:
			raise anyio.exceptions.ClosedResourceError
		return data

	async def close(self): await self.stream.close()
	async def abort(self): await self.stream.close()
	
	def local_address(self):
		return self.stream.address
	def remote_address(self):
		return self.stream.peer_address
	
	def remote_certificate(self):
		try:
			cert = self.stream.getpeercert(True)
			if cert:
				return TLSCertificate.parse(cert, TYPE_DER)
		except anyio.exceptions.TLSRequired:
			pass


class TLSServer:
	def __init__(self, handler, server, group):
		self.handler = handler
		self.server = server
		self.group = group
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.group.cancel_scope.cancel()
		await self.server.close()
	
	async def start(self):
		await self.group.spawn(self.serve)
		
	async def serve(self):
		while True:
			try:
				sock = await self.server.accept()
			except (OSError, ssl.SSLError) as e:
				logger.error("Failed to accept TLS connection: %s", e)
			else:
				client = TLSClient(sock)
				
				host, port = client.remote_address()
				logger.debug("New TLS connection: %s:%i", host, port)
				
				await self.group.spawn(self.handle, client)
	
	async def handle(self, client):
		with util.catch_all():
			async with client:
				await self.handler(client)


@contextlib.asynccontextmanager
async def connect(host, port, context=None):
	logger.debug("Connecting TLS client to %s:%s", host, port)
	if context is None:
		stream = await anyio.connect_tcp(host, port)
	else:
		stream = await anyio.connect_tcp(
			host, port, ssl_context=context.get(False), autostart_tls=True,
			tls_standard_compatible=False
		)
	async with TLSClient(stream) as client:
		yield client
	logger.debug("TLS client is closed")

@contextlib.asynccontextmanager
async def serve(handler, host="", port=0, context=None):
	if not host:
		host = util.local_address()
	logger.info("Starting TLS server at %s:%i", host, port)
	if context is None:
		server = await anyio.create_tcp_server(port, host)
	else:
		server = await anyio.create_tcp_server(
			port, host, context.get(True), tls_standard_compatible=False
		)
	async with anyio.create_task_group() as group:
		async with TLSServer(handler, server, group) as server:
			await server.start()
			yield
	logger.info("TLS server is closed")
