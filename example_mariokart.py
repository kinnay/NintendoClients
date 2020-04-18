
from nintendo.nex import backend, authentication, ranking, datastore
from nintendo.games import MK8
from nintendo import nnas
import requests

import logging
logging.basicConfig(level=logging.INFO)

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x250
REGION_ID = 4
COUNTRY_ID = 94
REGION_NAME = "EUR"
COUNTRY_NAME = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password

TRACK_ID = 27 #Mario Kart Stadium


nnas = nnas.NNASClient()
nnas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_NAME)
nnas.set_title(MK8.TITLE_ID_EUR, MK8.LATEST_VERSION)
nnas.login(USERNAME, PASSWORD)

nex_token = nnas.get_nex_token(MK8.GAME_SERVER_ID)

backend = backend.BackEndClient()
backend.configure(MK8.ACCESS_KEY, MK8.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password)

ranking_client = ranking.RankingClient(backend.secure_client)

order_param = ranking.RankingOrderParam()
order_param.order_calc = ranking.RankingOrderCalc.ORDINAL
order_param.offset = 499 #Start at 500th place
order_param.count = 20 #Download 20 highscores

rankings = ranking_client.get_ranking(
	ranking.RankingMode.GLOBAL, TRACK_ID,
	order_param, 0, 0
)

stats = ranking_client.get_stats(
	TRACK_ID, order_param, ranking.RankingStatFlags.ALL
).stats

def format_time(score):
	millisec = score % 1000
	seconds = score // 1000 % 60
	minutes = score // 1000 // 60
	return "%i:%02i.%03i" %(minutes, seconds, millisec)
	
names = nnas.get_nnids([data.pid for data in rankings.data])

#Print some interesting stats
print("Total:", int(stats[0]))
print("Total time:", format_time(stats[1]))
print("Average time:", format_time(stats[2]))
print("Lowest time:", format_time(stats[3]))
print("Highest time:", format_time(stats[4]))

print("Rankings:")
for rankdata in rankings.data:
	time = format_time(rankdata.score)
	print("\t%5i   %20s   %s" %(rankdata.rank, names[rankdata.pid], time))
	
#Let's download the replay file of whoever is in 500th place
store = datastore.DataStoreClient(backend.secure_client)

rankdata = rankings.data[0]
get_param = datastore.DataStorePrepareGetParam()
get_param.persistence_target.owner_id = rankdata.pid
get_param.persistence_target.persistence_id = TRACK_ID - 16
get_param.extra_data = ["WUP", str(REGION_ID), REGION_NAME, str(COUNTRY_ID), COUNTRY_NAME, ""]

req_info = store.prepare_get_object(get_param)
headers = {header.key: header.value for header in req_info.headers}
replay_data = requests.get("http://" + req_info.url, headers=headers).content

with open("replay.bin", "wb") as f:
	f.write(replay_data)

#Close connection
backend.close()
