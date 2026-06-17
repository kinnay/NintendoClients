
from nintendo import resources
from typing import Any


class Settings:
	TRANSPORT_UDP = 0
	TRANSPORT_TCP = 1
	TRANSPORT_WEBSOCKET = 2

	COMPRESSION_NONE = 0
	COMPRESSION_ZLIB = 1

	ENCRYPTION_NONE = 0
	ENCRYPTION_RC4 = 1
	
	_field_types = {
		"nex.version": int,
		"nex.client_version": int,
		"nex.struct_header": int,
		"nex.pid_size": int,
		
		"prudp.access_key": str,
		
		"prudp.version": int,
		"prudp.minor_version": int,
		"prudp.supported_functions": int,
		
		"prudp.transport": int,
		"prudp.compression": int,
		"prudp.encryption": int,
		
		"prudp.resend_timeout": float,
		"prudp.resend_limit": int,
		"prudp.ping_timeout": float,
		
		"prudp.fragment_size": int,
		"prudp.max_substream_id": int,
		
		"prudp_v0.signature_version": int,
		"prudp_v0.flags_version": int,
		"prudp_v0.checksum_version": int,

		"kerberos.key_size": int,
		"kerberos.key_derivation": int,
		"kerberos.ticket_version": int
	}

	_settings: dict[str, Any]
	
	def __init__(self, filename=None):
		self._settings = {}

		self.reset()
		if filename:
			self.load(filename)
		
	def __getitem__(self, name: str) -> Any:
		return self._settings[name]
	
	def __setitem__(self, name: str, value: Any) -> None:
		if name not in self._field_types:
			raise KeyError(f"Unknown setting: {name}")
		self._settings[name] = self._field_types[name](value)
	
	def configure(
		self, access_key: str, nex_version: int,
		client_version: int | None = None
	) -> None:
		self["prudp.access_key"] = access_key
		self["nex.version"] = nex_version
		if nex_version >= 40400:
			if client_version is None:
				raise ValueError("NEX 4.4.0 or later requires client version")
			self["nex.client_version"] = client_version
		
	def reset(self) -> None:
		self.load("default")
	
	def copy(self) -> Settings:
		copy = Settings()
		copy._settings = self._settings.copy()
		return copy

	def load(self, name: str) -> None:
		with resources.open(f"files/config/{name}.cfg") as f:
			linenum = 1
			for line in f:
				line = line.strip()
				if line:
					if "=" in line:
						field, value = line.split("=", 1)
						self[field.strip()] = value.strip()
					else:
						raise ValueError(f"Syntax error at line {linenum}")
				linenum += 1
				
				
def default():
	return Settings()

def load(name):
	return Settings(name)
