
from nintendo.games import SMM2
from nintendo.pia import lan

import logging
logging.basicConfig(level=logging.INFO)


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
	print("\t-----")


browser = lan.LANBrowser("switch.cfg", SMM2.PIA_KEY)
browser.configure(SMM2.PIA_VERSION)

search_criteria = lan.LanSessionSearchCriteria()

sessions = browser.browse(search_criteria)
if sessions:
	print("LAN sessions found:")
	for session in sessions:
		print_session_info(session)
else:
	print("No LAN session found")
