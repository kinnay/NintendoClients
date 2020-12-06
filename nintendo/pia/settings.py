

WIIU = 0
SWITCH = 1


class Settings:
	MODE_ECB = 0
	MODE_GCM = 1
	
	field_types = {
		"pia.version": int,
		"pia.system_version": int,
		"pia.application_version": int,
		"pia.lan_version": int,
		
		"common.pid_size": int
	}
	
	def __init__(self, version, app_version=-1, *, platform=SWITCH):
		self.settings = {}
		
		version //= 100
		self["pia.version"] = version
		self["pia.system_version"] = self.system_version(version)
		self["pia.application_version"] = app_version
		self["pia.lan_version"] = self.lan_version(version)
		
		self["common.pid_size"] = 8 if platform == SWITCH else 4
	
	def __getitem__(self, name): return self.settings[name]
	def __setitem__(self, name, value):
		if name not in self.field_types:
			raise KeyError("Unknown setting: %s" %name)
		self.settings[name] = self.field_types[name](value)
	
	def system_version(self, version):
		if version <= 503: return 0
		if version == 509: return 5
		if version == 510: return 6
		if 511 <= version <= 518: return 7
		if 519 <= version <= 529: return 8
		raise ValueError("Unsupported pia version")
	
	def lan_version(self, version):
		if version < 509: return 0
		if version < 511: return 1
		return 2

def default(version, app_version=-1, *, platform=SWITCH):
	return Settings(version, app_version, platform=platform)
