
# Module: <code>nintendo.nex.ranking2</code>

Provides a client and server for the `Ranking2Protocol`. This page was generated automatically from `ranking2.proto`.

<code>**class** [Ranking2Client](#ranking2client)</code><br>
<span class="docs">The client for the `Ranking2Protocol`.</span>

<code>**class** [Ranking2Server](#ranking2server)</code><br>
<span class="docs">The server for the `Ranking2Protocol`.</span>

<code>**class** [RankingMode](#rankingmode)</code><br>

<code>**class** [Ranking2CategorySetting](#ranking2categorysetting)([Structure](../common))</code><br>
<code>**class** [Ranking2ChartInfo](#ranking2chartinfo)([Structure](../common))</code><br>
<code>**class** [Ranking2ChartInfoInput](#ranking2chartinfoinput)([Structure](../common))</code><br>
<code>**class** [Ranking2CommonData](#ranking2commondata)([Structure](../common))</code><br>
<code>**class** [Ranking2EstimateScoreRankInput](#ranking2estimatescorerankinput)([Structure](../common))</code><br>
<code>**class** [Ranking2EstimateScoreRankOutput](#ranking2estimatescorerankoutput)([Structure](../common))</code><br>
<code>**class** [Ranking2GetByListParam](#ranking2getbylistparam)([Structure](../common))</code><br>
<code>**class** [Ranking2GetParam](#ranking2getparam)([Structure](../common))</code><br>
<code>**class** [Ranking2Info](#ranking2info)([Structure](../common))</code><br>
<code>**class** [Ranking2RankData](#ranking2rankdata)([Structure](../common))</code><br>
<code>**class** [Ranking2ScoreData](#ranking2scoredata)([Structure](../common))</code><br>

## Ranking2Client
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`Ranking2Client`](#ranking2client).</span>

<code>**async def put_score**(socres: list[[Ranking2ScoreData](#ranking2scoredata)], unique_id: int) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def get_common_data**(option_flags: int, pid: int, unique_id: int) -> [Ranking2CommonData](#ranking2commondata)</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def put_common_data**(data: [Ranking2CommonData](#ranking2commondata), unique_id: int) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def delete_common_data**(unique_id: int) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def get_ranking**(param: [Ranking2GetParam](#ranking2getparam)) -> [Ranking2Info](#ranking2info)</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_ranking_by_principal_id**(param: [Ranking2GetByListParam](#ranking2getbylistparam), pids: list[int]) -> [Ranking2Info](#ranking2info)</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def get_category_setting**(category: int) -> [Ranking2CategorySetting](#ranking2categorysetting)</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def get_ranking_chart**(input: [Ranking2ChartInfoInput](#ranking2chartinfoinput)) -> [Ranking2ChartInfo](#ranking2chartinfo)</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_ranking_charts**(inputs: list[[Ranking2ChartInfoInput](#ranking2chartinfoinput)]) -> list[[Ranking2ChartInfo](#ranking2chartinfo)]</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def get_estimate_score_rank**(input: [Ranking2EstimateScoreRankInput](#ranking2estimatescorerankinput)) -> [Ranking2EstimateScoreRankOutput](#ranking2estimatescorerankoutput)</code><br>
<span class="docs">Calls method `10` on the server.</span>

## Ranking2Server
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`Ranking2Server`](#ranking2server).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def put_score**(client: [RMCClient](../rmc#rmcclient), socres: list[[Ranking2ScoreData](#ranking2scoredata)], unique_id: int) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def get_common_data**(client: [RMCClient](../rmc#rmcclient), option_flags: int, pid: int, unique_id: int) -> [Ranking2CommonData](#ranking2commondata)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def put_common_data**(client: [RMCClient](../rmc#rmcclient), data: [Ranking2CommonData](#ranking2commondata), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def delete_common_data**(client: [RMCClient](../rmc#rmcclient), unique_id: int) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking**(client: [RMCClient](../rmc#rmcclient), param: [Ranking2GetParam](#ranking2getparam)) -> [Ranking2Info](#ranking2info)</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking_by_principal_id**(client: [RMCClient](../rmc#rmcclient), param: [Ranking2GetByListParam](#ranking2getbylistparam), pids: list[int]) -> [Ranking2Info](#ranking2info)</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def get_category_setting**(client: [RMCClient](../rmc#rmcclient), category: int) -> [Ranking2CategorySetting](#ranking2categorysetting)</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking_chart**(client: [RMCClient](../rmc#rmcclient), input: [Ranking2ChartInfoInput](#ranking2chartinfoinput)) -> [Ranking2ChartInfo](#ranking2chartinfo)</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_ranking_charts**(client: [RMCClient](../rmc#rmcclient), inputs: list[[Ranking2ChartInfoInput](#ranking2chartinfoinput)]) -> list[[Ranking2ChartInfo](#ranking2chartinfo)]</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def get_estimate_score_rank**(client: [RMCClient](../rmc#rmcclient), input: [Ranking2EstimateScoreRankInput](#ranking2estimatescorerankinput)) -> [Ranking2EstimateScoreRankOutput](#ranking2estimatescorerankoutput)</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

## RankingMode
This class defines the following constants:<br>
<span class="docs">
`GLOBAL_AROUND_SELF = 1`<br>
`GLOBAL = 2`<br>
`FRIENDS = 3`<br>
</span>

## Ranking2CategorySetting
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2CategorySetting` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>min_score: int</code><br>
<code>max_score: int</code><br>
<code>lowest_rank: int</code><br>
<code>reset_month: int</code><br>
<code>reset_day: int</code><br>
<code>reset_hour: int</code><br>
<code>reset_mode: int</code><br>
<code>max_seasons_to_go_back: int</code><br>
<code>score_order: bool</code><br>
</span><br>

## Ranking2ChartInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2ChartInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>create_time: [DateTime](../common#datetime)</code><br>
<code>index: int</code><br>
<code>category: int</code><br>
<code>season: int</code><br>
<code>bins_size: int</code><br>
<code>sampling_rate: int</code><br>
<code>score_order: bool</code><br>
<code>estimate_length: int</code><br>
<code>estimate_highest_score: int</code><br>
<code>estimate_lowest_score: int</code><br>
<code>estimate_median_score: int</code><br>
<code>estimate_average_score: float</code><br>
<code>highest_bins_score: int</code><br>
<code>lowest_bins_score: int</code><br>
<code>bins_width: int</code><br>
<code>attribute1: int</code><br>
<code>attribute2: int</code><br>
<code>quantities: list[int]</code><br>
</span><br>

## Ranking2ChartInfoInput
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2ChartInfoInput` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>chart_index: int</code><br>
<code>seasons_to_go_back: int</code><br>
</span><br>

## Ranking2CommonData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2CommonData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>username: str</code><br>
<code>mii: bytes</code><br>
<code>binary_data: bytes</code><br>
</span><br>

## Ranking2EstimateScoreRankInput
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2EstimateScoreRankInput` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>category: int</code><br>
<code>seasons_to_go_back: int</code><br>
<code>score: int</code><br>
</span><br>

## Ranking2EstimateScoreRankOutput
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2EstimateScoreRankOutput` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>rank: int</code><br>
<code>length: int</code><br>
<code>score: int</code><br>
<code>category: int</code><br>
<code>season: int</code><br>
</span><br>

## Ranking2GetByListParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2GetByListParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>category: int</code><br>
<code>offset: int</code><br>
<code>length: int</code><br>
<code>sort_flags: int</code><br>
<code>option_flags: int</code><br>
<code>seasons_to_go_back: int</code><br>
</span><br>

## Ranking2GetParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2GetParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unique_id: int = 0</code><br>
<code>pid: int = 0</code><br>
<code>category: int</code><br>
<code>offset: int = 0</code><br>
<code>count: int = 10</code><br>
<code>sort_flags: int = 0</code><br>
<code>option_flags: int = 0</code><br>
<code>mode: int = 2</code><br>
<code>seasons_to_go_back: int = 0</code><br>
</span><br>

## Ranking2Info
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2Info` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data: list[[Ranking2RankData](#ranking2rankdata)]</code><br>
<code>lowest_rank: int</code><br>
<code>num_entries: int</code><br>
<code>season: int</code><br>
</span><br>

## Ranking2RankData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2RankData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>misc: int</code><br>
<code>unique_id: int</code><br>
<code>pid: int</code><br>
<code>rank: int</code><br>
<code>score: int</code><br>
<code>common_data: [Ranking2CommonData](#ranking2commondata) = [Ranking2CommonData](#ranking2commondata)()</code><br>
</span><br>

## Ranking2ScoreData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Ranking2ScoreData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>misc: int</code><br>
<code>category: int</code><br>
<code>score: int</code><br>
</span><br>

