
from anynet import tls
import importlib.resources

def get(path):
	return importlib.resources.files("nintendo").joinpath(path)

def open(path, mode="r", *, encoding="utf-8"):
	return get(path).open(mode, encoding=encoding)

def read_bytes(path):
	return get(path).read_bytes()

def certificate(name):
	data = read_bytes("files/cert/%s" %name)
	return tls.TLSCertificate.parse(data, tls.TYPE_DER)

def private_key(name):
	data = read_bytes("files/cert/%s" %name)
	return tls.TLSPrivateKey.parse(data, tls.TYPE_DER)
