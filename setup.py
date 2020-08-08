
from distutils.core import setup

setup(
	name="Nintendo",
	description="Client for Nintendo game servers",
	url="https://github.com/Kinnay/NintendoClients",
	packages=[
		"nintendo", "nintendo.common", "nintendo.enl",
		"nintendo.nex", "nintendo.pia"
	],
	package_data={"nintendo": ["files/config/*", "files/cert/*"]},
	install_requires=[
		'anyio',
		'cryptography',
		'pyopenssl',
		'netifaces',
		'pycryptodome'
	]
)
