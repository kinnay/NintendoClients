
from nintendo.games import SMM2
from nintendo.pia import lan, settings
import anyio

import logging
logging.basicConfig(level=logging.INFO)


roles = {
	1: "HOST",
	2: "PLAYER"
}

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
			role = roles[player.role]
			print("\t\t<%s, %i, %s>" %(player.username, player.id, role))
	print("\tHost: %s" %info.host_location.get_station_url())
	print("\t-----")


async def main():
	search_criteria = lan.LanSessionSearchCriteria()
	
	s = settings.default(SMM2.PIA_VERSION)
	sessions = await lan.browse(s, search_criteria, SMM2.PIA_KEY)
	if sessions:
		print("LAN sessions found:")
		for session in sessions:
			print_session_info(session)
	else:
		print("No LAN session found")

anyio.run(main)
