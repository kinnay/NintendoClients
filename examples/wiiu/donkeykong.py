
from nintendo.nex import backend, ranking, datastore, settings
from nintendo import nnas
from anynet import http
import anyio

import logging
logging.basicConfig(level=logging.INFO)


DEVICE_ID = 12345678 #From MCP_GetDeviceId
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x270
REGION = 4 #EUR
COUNTRY = "NL"
LANGUAGE = "en"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password

TITLE_ID = 0x0005000010138300
TITLE_VERSION = 17

GAME_SERVER_ID = 0x10144800
ACCESS_KEY = "7fcf384a"
NEX_VERSION = 30400


async def main():
	nas = nnas.NNASClient()
	nas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
	nas.set_title(TITLE_ID, TITLE_VERSION)
	nas.set_locale(REGION, COUNTRY, LANGUAGE)
	
	access_token = await nas.login(USERNAME, PASSWORD)
	nex_token = await nas.get_nex_token(access_token.token, GAME_SERVER_ID)

	s = settings.default()
	s.configure(ACCESS_KEY, NEX_VERSION)
	async with backend.connect(s, nex_token.host, nex_token.port) as be:
		async with be.login(str(nex_token.pid), nex_token.password) as client:
			order_param = ranking.RankingOrderParam()
			order_param.offset = 0 #Start with the world record
			order_param.count = 20 #Download 20 highscores

			ranking_client = ranking.RankingClient(client)
			rankings = await ranking_client.get_ranking(
				ranking.RankingMode.GLOBAL, #Get the global leaderboard
				0x893EB726, #Category, this is 3-A (Magrove Cove)
				order_param,
				0, 0
			)
		
			print("Total:", rankings.total)
			print("Rankings:")
			for rankdata in rankings.data:
				seconds = (rankdata.score >> 1) / 60
				time = "%i:%02i.%02i" %(seconds / 60, seconds % 60, (seconds * 100) % 100)
				damage = " Damaged " if rankdata.score & 1 else "No damage"
				kong = ["No Kong", "Diddy", "Dixie", "Cranky"][rankdata.groups[1]]
				name = rankdata.common_data.decode("ascii")[:-1]
		
				print("\t%2i   %20s   %s (%s)   %s" %(rankdata.rank, name, time, damage, kong))
				
				
			#Now download the world record replay file if available
			world_record = rankings.data[0]
			if world_record.param: #If world record has a replay file	
				store = datastore.DataStoreClient(client)
				
				get_param = datastore.DataStorePrepareGetParam()
				get_param.data_id = world_record.param
				
				req_info = await store.prepare_get_object(get_param)
				headers = {header.key: header.value for header in req_info.headers}
				response = await http.get(req_info.url, headers=headers)
				response.raise_if_error()
				
				with open("replay.bin", "wb") as f:
					f.write(response.body)

anyio.run(main)
