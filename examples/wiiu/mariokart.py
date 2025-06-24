from nintendo.nex import backend, ranking, datastore, settings
from nintendo import nnas
from anynet import http
import anyio

import logging

logging.basicConfig(level=logging.INFO)


DEVICE_ID = 12345678  # From MCP_GetDeviceId
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x270
REGION_ID = 4  # EU
COUNTRY_ID = 94  # NL
REGION_NAME = "EUR"
COUNTRY_NAME = "NL"
LANGUAGE = "en"

USERNAME = "..."  # Nintendo network id
PASSWORD = "..."  # Nintendo network password

TRACK_ID = 27  # Mario Kart Stadium

TITLE_ID = 0x000500001010ED00
TITLE_VERSION = 64

GAME_SERVER_ID = 0x1010EB00
ACCESS_KEY = "25dbf96a"
NEX_VERSION = 30504


def format_time(score):
	millisec = score % 1000
	seconds = score // 1000 % 60
	minutes = score // 1000 // 60
	return "%i:%02i.%03i" % (minutes, seconds, millisec)


async def main():
	nas = nnas.NNASClient()
	nas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
	nas.set_title(TITLE_ID, TITLE_VERSION)
	nas.set_locale(REGION_ID, COUNTRY_NAME, LANGUAGE)

	access_token = await nas.login(USERNAME, PASSWORD)
	nex_token = await nas.get_nex_token(access_token.token, GAME_SERVER_ID)

	s = settings.default()
	s.configure(ACCESS_KEY, NEX_VERSION)
	async with backend.connect(s, nex_token.host, nex_token.port) as be:
		async with be.login(str(nex_token.pid), nex_token.password) as client:
			ranking_client = ranking.RankingClient(client)

			order_param = ranking.RankingOrderParam()
			order_param.order_calc = ranking.RankingOrderCalc.ORDINAL
			order_param.offset = 499  # Start at 500th place
			order_param.count = 20  # Download 20 highscores

			rankings = await ranking_client.get_ranking(
				ranking.RankingMode.GLOBAL, TRACK_ID, order_param, 0, 0
			)

			ranking_stats = await ranking_client.get_stats(
				TRACK_ID, order_param, ranking.RankingStatFlags.ALL
			)

			names = await nas.get_nnids([data.pid for data in rankings.data])

			# Print some interesting stats
			stats = ranking_stats.stats
			print("Total:", int(stats[0]))
			print("Total time:", format_time(stats[1]))
			print("Lowest time:", format_time(stats[2]))
			print("Highest time:", format_time(stats[3]))
			print("Average time:", format_time(stats[4]))

			print("Rankings:")
			for rankdata in rankings.data:
				time = format_time(rankdata.score)
				print("\t%5i   %20s   %s" % (rankdata.rank, names[rankdata.pid], time))

			# Let's download the replay file of whoever is in 500th place
			store = datastore.DataStoreClient(client)

			rankdata = rankings.data[0]
			get_param = datastore.DataStorePrepareGetParam()
			get_param.persistence_target.owner_id = rankdata.pid
			get_param.persistence_target.persistence_id = TRACK_ID - 16
			get_param.extra_data = [
				"WUP",
				str(REGION_ID),
				REGION_NAME,
				str(COUNTRY_ID),
				COUNTRY_NAME,
				"",
			]

			req_info = await store.prepare_get_object(get_param)
			headers = {header.key: header.value for header in req_info.headers}
			response = await http.get(req_info.url, headers=headers)
			response.raise_if_error()

			with open("replay.bin", "wb") as f:
				f.write(response.body)


anyio.run(main)
