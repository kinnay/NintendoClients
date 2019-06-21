
import pkg_resources


class Settings:

	TRANSPORT_UDP = 0
	TRANSPORT_TCP = 1
	TRANSPORT_WEBSOCKET = 2
	
	field_types = {
		"prudp.transport": int,
		"prudp.version": int,
		"prudp.minor_version": int,
		"prudp.stream_type": int,
		"prudp.fragment_size": int,
		"prudp.resend_timeout": float,
		"prudp.resend_limit": int,
		"prudp.ping_timeout": float,
		"prudp.substreams": int,
		"prudp.compression": int,
		
		"prudp_v0.signature_version": int,
		"prudp_v0.flags_version": int,
		"prudp_v0.checksum_version": int,

		"kerberos.key_size": int,
		"kerberos.key_derivation": int,
		
		"common.pid_size": int,
		
		"server.version": int,
		"server.access_key": str.encode,
		
		"pia.station_extension": int,
		"pia.crypto_enabled": int,
		"pia.crypto_required": int
	}

	def __init__(self, filename=None):
		self.settings = {}
		self.reset()
		if filename:
			self.load(filename)
		
	def reset(self): self.load("default.cfg")
	def copy(self):
		copy = Settings()
		copy.settings = self.settings.copy()
		return copy
	
	def get(self, field): return self.settings[field]
	def set(self, field, value):
		if field not in self.field_types:
			raise ValueError("Unknown setting: %s" %field)
		self.settings[field] = self.field_types[field](value)

	def load(self, filename):
		filename = pkg_resources.resource_filename("nintendo", "files/config/%s" %filename)
		with open(filename) as f:
			linenum = 1
			for line in f:
				line = line.strip()
				if line:
					if "=" in line:
						field, value = line.split("=", 1)
						self.set(field.strip(), value.strip())
					else:
						raise ValueError("Syntax error at line %i" %linenum)
				linenum += 1
