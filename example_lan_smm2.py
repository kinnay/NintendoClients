
from nintendo.sead import random
from nintendo.enl import crypto
from nintendo.pia import lan
from nintendo import settings

def print_session_info(info):
	print("\tGame mode: %i" %info.game_mode)
	print("\tSession id: %i" %info.session_id)
	print("\tAttributes: %s" %info.attributes)
	print("\tCurrent number of players: %i" %info.num_participants)
	print("\tMinimum number of players: %i" %info.min_participants)
	print("\tMaximum number of players: %i" %info.max_participants)
	print("\tSystem communication version: %i" %info.system_version)
	print("\tApplication communication version: %i" %info.application_version)
	print("\tSession type: %i" %info.session_type)
	print("\tApplication data: <%i bytes>" %len(info.application_data))
	print("\tIs opened: %s" %info.is_opened)
	print("\tPlayers:")
	for player in info.players:
		if player.id != 0:
			print("\t\t<%i, %s, %i>" %(player.role, player.username, player.id))
	print("\tHost: %s" %info.host_location.get_station_url())


rand = random.Random(0x123)
table = [
	0xB301CA48, 0x5E758911, 0xC2B349E2, 0xF9942930,
	0x447AEFC0, 0xB6B5DB5F, 0xEE116832, 0xB6940169,
	0x2503FC94, 0x3D74B448, 0x58411B2C, 0x4EC8C604,
	0x74157415, 0xEC5B582B, 0xBC93A6F7, 0xB463AF87,
	0x6B09D0C2, 0x5DA54788, 0x7C20F6D5, 0xD5967141,
	0xF03C24F1, 0x87D2A479, 0xFC3F7C08, 0x9A4506B7,
	0x8B4FA2A2, 0x99AC2EDE, 0x9E74DEDF, 0x2CB60318,
	0xDA1AEE9E, 0x2238F1DD, 0x1A825163, 0x86B03FE8,
	0x8BD35FBE, 0x6E80E100, 0x6681ACFA, 0x61C990BD,
	0x70F61D95, 0x19177A6A, 0x729AE3CE, 0x5FFBD958,
	0x9F217D87, 0x3D478023, 0x986690D6, 0x19D6AB9B,
	0x8D8F2063, 0x8CC8EF69, 0x20843E06, 0x8CA2C3FE,
	0x78DA6631, 0xB3A27DE4, 0xB2D71198, 0x28F0890F,
	0x83B089CE, 0x235D8901, 0x290C0723, 0x85184BFC,
	0x82E15C68, 0x4D3BD8B4, 0x0447FB2F, 0x434717F0,
	0xCBCD01EC, 0x58A09E59, 0x630588E1, 0x1886EBE6
]
key = crypto.create_key(rand, table, 16)

settings = settings.Settings("switch.cfg")
settings.set("pia.version", 51800)
settings.set("pia.lan_version", 2)

browser = lan.LanBrowser(settings, key)

search_criteria = lan.LanSessionSearchCriteria()

sessions = browser.browse(search_criteria)
if sessions:
	print("LAN sessions found:")
	for session in sessions:
		print_session_info(session)
else:
	print("No LAN session found")
