
# Module: <code>nintendo.nex.ranking_mk8d</code>

Provides a client and server for the `RankingProtocolMK8D`. This page was generated automatically from `ranking_mk8d.proto`.

<code>**class** [RankingClientMK8D](#rankingclientmk8d)</code><br>
<span class="docs">The client for the `RankingProtocolMK8D`.</span>

<code>**class** [RankingServerMK8D](#rankingservermk8d)</code><br>
<span class="docs">The server for the `RankingProtocolMK8D`.</span>

<code>**class** [RankingMode](#rankingmode)</code><br>
<code>**class** [RankingOrderCalc](#rankingordercalc)</code><br>
<code>**class** [RankingStatFlags](#rankingstatflags)</code><br>

<code>**class** [CommonDataList](#commondatalist)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingGetScoreParam](#competitionrankinggetscoreparam)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingInfo](#competitionrankinginfo)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingInfoGetParam](#competitionrankinginfogetparam)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingScoreData](#competitionrankingscoredata)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingScoreInfo](#competitionrankingscoreinfo)([Structure](common.md))</code><br>
<code>**class** [CompetitionRankingUploadScoreParam](#competitionrankinguploadscoreparam)([Structure](common.md))</code><br>
<code>**class** [RankingCachedResult](#rankingcachedresult)([RankingResult](#rankingresult))</code><br>
<code>**class** [RankingChangeAttributesParam](#rankingchangeattributesparam)([Structure](common.md))</code><br>
<code>**class** [RankingOrderParam](#rankingorderparam)([Structure](common.md))</code><br>
<code>**class** [RankingRankData](#rankingrankdata)([Structure](common.md))</code><br>
<code>**class** [RankingResult](#rankingresult)([Structure](common.md))</code><br>
<code>**class** [RankingScoreData](#rankingscoredata)([Structure](common.md))</code><br>
<code>**class** [RankingStats](#rankingstats)([Structure](common.md))</code><br>

## RankingClientMK8D
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`RankingClientMK8D`](#rankingclientmk8d).</span>

<code>**async def upload_score**(score_data: [RankingScoreData](#rankingscoredata), unique_id: int) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def delete_score**(category: int, unique_id: int) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def delete_all_scores**(unique_id: int) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def upload_common_data**(common_data: bytes, unique_id: int) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def delete_common_data**(unique_id: int) -> None</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_common_data**(unique_id: int) -> bytes</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def change_attributes**(category: int, param: [RankingChangeAttributesParam](#rankingchangeattributesparam), unique_id: int) -> None</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def change_all_attributes**(param: [RankingChangeAttributesParam](#rankingchangeattributesparam), unique_id: int) -> None</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_ranking**(mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int, pid: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def get_approx_order**(category: int, order: [RankingOrderParam](#rankingorderparam), score: int, unique_id: int, pid: int) -> int</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def get_stats**(category: int, order: [RankingOrderParam](#rankingorderparam), flags: int) -> [RankingStats](#rankingstats)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def get_ranking_by_pid_list**(pids: list[int], mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def get_ranking_by_unique_id_list**(ids: list[int], mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def get_cached_topx_ranking**(category: int, order: [RankingOrderParam](#rankingorderparam)) -> [RankingCachedResult](#rankingcachedresult)</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def get_cached_topx_rankings**(categories: list[int], order: list[[RankingOrderParam](#rankingorderparam)]) -> list[[RankingCachedResult](#rankingcachedresult)]</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def get_competition_ranking_score**(param: [CompetitionRankingGetScoreParam](#competitionrankinggetscoreparam)) -> list[[CompetitionRankingScoreInfo](#competitionrankingscoreinfo)]</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def upload_competition_ranking_score**(param: [CompetitionRankingUploadScoreParam](#competitionrankinguploadscoreparam)) -> bool</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def get_competition_info**(param: [CompetitionRankingInfoGetParam](#competitionrankinginfogetparam)) -> list[[CompetitionRankingInfo](#competitionrankinginfo)]</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def upload_score_pack**(score_data: [RankingScoreData](#rankingscoredata), metadata: bytes) -> None</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def get_commmon_data_by_pid_list**(pids: list[int]) -> [CommonDataList](#commondatalist)</code><br>
<span class="docs">Calls method `22` on the server.</span>

## RankingServerMK8D
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`RankingServerMK8D`](#rankingservermk8d).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def upload_score**(client: [RMCClient](rmc.md#rmcclient), score_data: [RankingScoreData](#rankingscoredata), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def delete_score**(client: [RMCClient](rmc.md#rmcclient), category: int, unique_id: int) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def delete_all_scores**(client: [RMCClient](rmc.md#rmcclient), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def upload_common_data**(client: [RMCClient](rmc.md#rmcclient), common_data: bytes, unique_id: int) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def delete_common_data**(client: [RMCClient](rmc.md#rmcclient), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_common_data**(client: [RMCClient](rmc.md#rmcclient), unique_id: int) -> bytes</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def change_attributes**(client: [RMCClient](rmc.md#rmcclient), category: int, param: [RankingChangeAttributesParam](#rankingchangeattributesparam), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def change_all_attributes**(client: [RMCClient](rmc.md#rmcclient), param: [RankingChangeAttributesParam](#rankingchangeattributesparam), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking**(client: [RMCClient](rmc.md#rmcclient), mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int, pid: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def get_approx_order**(client: [RMCClient](rmc.md#rmcclient), category: int, order: [RankingOrderParam](#rankingorderparam), score: int, unique_id: int, pid: int) -> int</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def get_stats**(client: [RMCClient](rmc.md#rmcclient), category: int, order: [RankingOrderParam](#rankingorderparam), flags: int) -> [RankingStats](#rankingstats)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking_by_pid_list**(client: [RMCClient](rmc.md#rmcclient), pids: list[int], mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking_by_unique_id_list**(client: [RMCClient](rmc.md#rmcclient), ids: list[int], mode: int, category: int, order: [RankingOrderParam](#rankingorderparam), unique_id: int) -> [RankingResult](#rankingresult)</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def get_cached_topx_ranking**(client: [RMCClient](rmc.md#rmcclient), category: int, order: [RankingOrderParam](#rankingorderparam)) -> [RankingCachedResult](#rankingcachedresult)</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def get_cached_topx_rankings**(client: [RMCClient](rmc.md#rmcclient), categories: list[int], order: list[[RankingOrderParam](#rankingorderparam)]) -> list[[RankingCachedResult](#rankingcachedresult)]</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def get_competition_ranking_score**(client: [RMCClient](rmc.md#rmcclient), param: [CompetitionRankingGetScoreParam](#competitionrankinggetscoreparam)) -> list[[CompetitionRankingScoreInfo](#competitionrankingscoreinfo)]</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def upload_competition_ranking_score**(client: [RMCClient](rmc.md#rmcclient), param: [CompetitionRankingUploadScoreParam](#competitionrankinguploadscoreparam)) -> bool</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def get_competition_info**(client: [RMCClient](rmc.md#rmcclient), param: [CompetitionRankingInfoGetParam](#competitionrankinginfogetparam)) -> list[[CompetitionRankingInfo](#competitionrankinginfo)]</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def upload_score_pack**(client: [RMCClient](rmc.md#rmcclient), score_data: [RankingScoreData](#rankingscoredata), metadata: bytes) -> None</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def get_commmon_data_by_pid_list**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> [CommonDataList](#commondatalist)</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

## RankingMode
This class defines the following constants:<br>
<span class="docs">
`GLOBAL = 0`<br>
`GLOBAL_AROUND_SELF = 1`<br>
`SELF = 4`<br>
</span>

## RankingOrderCalc
This class defines the following constants:<br>
<span class="docs">
`STANDARD = 0`<br>
`ORDINAL = 1`<br>
</span>

## RankingStatFlags
This class defines the following constants:<br>
<span class="docs">
`RANKING_COUNT = 1`<br>
`TOTAL_SCORE = 2`<br>
`LOWEST_SCORE = 4`<br>
`HIGHEST_SCORE = 8`<br>
`AVERAGE_SCORE = 16`<br>
`ALL = 31`<br>
</span>

## CommonDataList
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CommonDataList` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data: list[bytes]</code><br>
</span><br>

## CompetitionRankingGetScoreParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingGetScoreParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>id: int</code><br>
<code>range: [ResultRange](common.md#resultrange) = [ResultRange](common.md#resultrange)()</code><br>
</span><br>

## CompetitionRankingInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>id: int</code><br>
<code>num_participants: int</code><br>
<code>team_scores: list[int]</code><br>
</span><br>

## CompetitionRankingInfoGetParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingInfoGetParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>rank_order: int</code><br>
<code>range: [ResultRange](common.md#resultrange) = [ResultRange](common.md#resultrange)()</code><br>
</span><br>

## CompetitionRankingScoreData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingScoreData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>rank: int</code><br>
<code>pid: int</code><br>
<code>score: int</code><br>
<code>last_update: [DateTime](common.md#datetime)</code><br>
<code>team_id: int = 255</code><br>
<code>metadata: bytes</code><br>
</span><br>

## CompetitionRankingScoreInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingScoreInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>season_id: int</code><br>
<code>scores: list[[CompetitionRankingScoreData](#competitionrankingscoredata)]</code><br>
<code>num_participants: int</code><br>
<code>team_scores: list[int]</code><br>
</span><br>

## CompetitionRankingUploadScoreParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CompetitionRankingUploadScoreParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: int</code><br>
<code>unk3: int</code><br>
<code>unk4: int</code><br>
<code>unk5: int</code><br>
<code>unk6: int</code><br>
<code>unk7: bool</code><br>
<code>metadata: bytes</code><br>
</span><br>

## RankingCachedResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingCachedResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>created_time: [DateTime](common.md#datetime)</code><br>
<code>expired_time: [DateTime](common.md#datetime)</code><br>
<code>max_length: int</code><br>
</span><br>

## RankingChangeAttributesParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingChangeAttributesParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>flags: int</code><br>
<code>groups: list[int]</code><br>
<code>param: int</code><br>
</span><br>

## RankingOrderParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingOrderParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>order_calc: int = 0</code><br>
<code>group_index: int = 255</code><br>
<code>group_num: int = 0</code><br>
<code>time_scope: int = 2</code><br>
<code>offset: int</code><br>
<code>count: int</code><br>
</span><br>

## RankingRankData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingRankData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>unique_id: int</code><br>
<code>rank: int</code><br>
<code>category: int</code><br>
<code>score: int</code><br>
<code>groups: list[int]</code><br>
<code>param: int</code><br>
<code>common_data: bytes</code><br>
If `nex.version` >= 40000:<br>
<span class="docs">
<code>update_time: [DateTime](common.md#datetime)</code><br>
</span><br>
</span><br>

## RankingResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data: list[[RankingRankData](#rankingrankdata)]</code><br>
<code>total: int</code><br>
<code>since_time: [DateTime](common.md#datetime)</code><br>
</span><br>

## RankingScoreData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingScoreData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>category: int</code><br>
<code>score: int</code><br>
<code>order: int</code><br>
<code>update_mode: int</code><br>
<code>groups: list[int]</code><br>
<code>param: int</code><br>
</span><br>

## RankingStats
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RankingStats` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>stats: list[float]</code><br>
</span><br>

