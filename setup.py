
from distutils.core import setup

setup(
	name = "Nintendo",
	description = "Client for Nintendo game servers",
	url = "https://github.com/Kinnay/NintendoClients",
	packages = ["nintendo", "nintendo.common", "nintendo.nex", "nintendo.pia"],
	package_data = {"nintendo": ["files/*.*"]}
)
