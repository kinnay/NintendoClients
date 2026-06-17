
from anynet import tls

import importlib.resources
import importlib.resources.abc


def get(path: str) -> importlib.resources.abc.Traversable:
	return importlib.resources.files("nintendo").joinpath(path)

def open(path: str):
	return get(path).open()

def read_bytes(path: str) -> bytes:
	return get(path).read_bytes()

def certificate(name: str) -> tls.TLSCertificate:
	data = read_bytes(f"files/cert/{name}")
	return tls.TLSCertificate.parse(data, tls.TYPE_DER)

def private_key(name: str) -> tls.TLSPrivateKey:
	data = read_bytes(f"files/cert/{name}")
	return tls.TLSPrivateKey.parse(data, tls.TYPE_DER)
