
from nintendo.nex import backend, authentication, ranking
from nintendo.games import MK8Deluxe

TRACK_ID = 10 #Sunshine airport

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %MK8Deluxe.GAME_SERVER_ID
PORT = 443

backend = backend.BackEndClient(
	MK8Deluxe.ACCESS_KEY, MK8Deluxe.NEX_VERSION, backend.Settings("switch.cfg")
)
backend.connect(HOST, PORT)
backend.login_guest()

ranking_client = ranking.RankingClient(backend)
rankings = ranking_client.get_ranking(
	ranking.RankingClient.MODE_GLOBAL,
	TRACK_ID,
	ranking.RankingOrderParam(
		ranking.RankingOrderParam.ORDINAL, #"1234" ranking
		0xFF, 0, 2,
		0, 20 #Download top 20
	),
	0, 0
)
stats = ranking_client.get_stats(
	TRACK_ID,
	ranking.RankingOrderParam(
		ranking.RankingOrderParam.ORDINAL, 0xFF, 0, 2, 0, 0
	)
)

def format_time(score):
	millisec = score % 1000
	seconds = score // 1000 % 60
	minutes = score // 1000 // 60
	return "%i:%02i.%03i" %(minutes, seconds, millisec)
	
#Print some interesting stats
print("Total:", int(stats[ranking.RankingClient.STAT_RANKING_COUNT]))
print("Total time:", format_time(stats[ranking.RankingClient.STAT_TOTAL_SCORE]))
print("Average time:", format_time(stats[ranking.RankingClient.STAT_AVERAGE_SCORE]))
print("Lowest time:", format_time(stats[ranking.RankingClient.STAT_LOWEST_SCORE]))
print("Highest time:", format_time(stats[ranking.RankingClient.STAT_HIGHEST_SCORE]))

print("Rankings:")
for rankdata in rankings.datas:
	time = format_time(rankdata.score)
	print("\t%5i   %016X   %s" %(rankdata.rank, rankdata.pid, time))

#Close connection
backend.close()
