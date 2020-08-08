
class Settings:
	field_types = {
		"pia.version": int,
		"pia.system_version": int,
		"pia.application_version": int,
		"pia.station_extension": bool,
		"pia.crypto_enabled": bool,
		"pia.encryption_method": int,
		"pia.signature_method": int,
		"pia.header_version": int,
		"pia.message_version": int,
		"pia.protocol_type_revision": int,
		"pia.lan_version": int,
		
		"common.pid_size": int
	}
	
	def __init__(self, version, app_version=-1):
		self.settings = {}
		
		self["pia.version"] = version
		self["pia.system_version"] = self.system_version(version)
		self["pia.application_version"] = app_version
		self["pia.station_extension"] = version < 50000
		self["pia.crypto_enabled"] = version >= 50900
		self["pia.encryption_method"] = 1 if version >= 50900 else 0
		self["pia.signature_method"] = 0 if version >= 50900 else 1
		self["pia.header_version"] = 4 if version >= 51100 else 0
		self["pia.message_version"] = self.message_version(version)
		self["pia.protocol_type_revision"] = 1 if version >= 509000 else 0
		self["pia.lan_version"] = self.lan_version(version)
		
		self["common.pid_size"] = 8 if version >= 50000 else 4
	
	def __getitem__(self, name): return self.settings[name]
	def __setitem__(self, name, value):
		if name not in self.field_types:
			raise KeyError("Unknown setting: %s" %name)
		self.settings[name] = self.field_types[name](value)
	
	def system_version(self, version):
		version = version // 100
		if version <= 503: return 0
		if version == 509: return 5
		if version == 510: return 6
		if 511 <= version <= 518: return 7
		if 519 <= version <= 529: return 8
		raise ValueError("Unsupported pia version")
		
	def message_version(self, version):
		version = version // 100
		if version <= 503: return 0
		if version in [509, 510]: return 1
		if version == 511: return 2
		if 514 <= version <= 517: return 3
		if version == 518: return 4
		raise ValueError("Unsupported pia version")
	
	def lan_version(self, version):
		if version < 50900: return 0
		if version < 51100: return 1
		return 2
