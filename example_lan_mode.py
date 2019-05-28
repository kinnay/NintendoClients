
from nintendo.enl import crypto
from nintendo.pia import lan
from nintendo import settings

def print_session_info(info):
	print("LAN session found:")
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
	print("\tSession param: %s" %info.session_param.hex())
	print("\tHost: %s" %info.host_location.get_station_url())


seed = 0xCEB9D8D9
table = [
	0x56CB956F, 0x7B50EEC6, 0x234D1A63, 0x1C691A6B,
	0xD2D9C482, 0xCFE21965, 0x0B32DF99, 0xB32AFE44,
	0xB15DA3D7, 0x86588505, 0x4FC8CD8B, 0xC30F864B,
	0x08D4D3BE, 0xEFDEC6CA, 0x63A1D53F, 0xC545538D,
	0x715E27A2, 0x4818A005, 0x8C28D9F8, 0xC303EABF,
	0xF1D847ED, 0xE837F303, 0xE68981E8, 0x63E2F9BC,
	0xC320F7E1, 0x5E0B4084, 0x502B2A2D, 0x65D36579,
	0x0D169E46, 0x65AB445D, 0xFDF0678B, 0x26167D3E,
	0xFE5025A0, 0x04EB0EA8, 0xC048B044, 0xF858002E,
	0x6725F7D6, 0xD4086AA8, 0xF216DE10, 0x0F1807E6,
	0xD3614878, 0x34A2FEE6, 0xA69AE3DE, 0xED8518EF,
	0x6FCCB7A5, 0x7F8D0E40, 0x9B72BFA8, 0x87C669D4,
	0x5BF80652, 0x9A71383F, 0xBA3E7A7A, 0x1ABA65A3,
	0xA9A16DFF, 0xD07B9E3C, 0x11C9BD45, 0xF14A6D81,
	0x78516ECD, 0x53445C15, 0xC86E9942, 0x5501D2C9,
	0xD0D4ECB3, 0x38F5C341, 0xC4A16155, 0x42F1F406
]
key = crypto.create_key(seed, table, 16)

settings = settings.Settings("switch.cfg")
browser = lan.LanBrowser(settings, key)

search_criteria = lan.LanSessionSearchCriteria()

result = browser.browse(search_criteria)
if result:
	print_session_info(result)
else:
	print("No LAN session found")
