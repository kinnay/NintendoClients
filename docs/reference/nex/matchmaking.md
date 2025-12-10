
# Module: <code>nintendo.nex.matchmaking</code>

Provides a client and server for the `MatchMakingProtocol`, `MatchMakingProtocolExt`, `MatchmakeExtensionProtocol` and `MatchmakeRefereeProtocol`. This page was generated automatically from `matchmaking.proto`.

<code>**class** [MatchMakingClient](#matchmakingclient)</code><br>
<span class="docs">The client for the `MatchMakingProtocol`.</span>

<code>**class** [MatchMakingClientExt](#matchmakingclientext)</code><br>
<span class="docs">The client for the `MatchMakingProtocolExt`.</span>

<code>**class** [MatchmakeExtensionClient](#matchmakeextensionclient)</code><br>
<span class="docs">The client for the `MatchmakeExtensionProtocol`.</span>

<code>**class** [MatchmakeRefereeClient](#matchmakerefereeclient)</code><br>
<span class="docs">The client for the `MatchmakeRefereeProtocol`.</span>

<code>**class** [MatchMakingServer](#matchmakingserver)</code><br>
<span class="docs">The server for the `MatchMakingProtocol`.</span>

<code>**class** [MatchMakingServerExt](#matchmakingserverext)</code><br>
<span class="docs">The server for the `MatchMakingProtocolExt`.</span>

<code>**class** [MatchmakeExtensionServer](#matchmakeextensionserver)</code><br>
<span class="docs">The server for the `MatchmakeExtensionProtocol`.</span>

<code>**class** [MatchmakeRefereeServer](#matchmakerefereeserver)</code><br>
<span class="docs">The server for the `MatchmakeRefereeProtocol`.</span>

<code>**class** [MatchmakeSystem](#matchmakesystem)</code><br>

<code>**class** [AutoMatchmakeParam](#automatchmakeparam)([Structure](common.md))</code><br>
<code>**class** [CreateMatchmakeSessionParam](#creatematchmakesessionparam)([Structure](common.md))</code><br>
<code>**class** [DeletionEntry](#deletionentry)([Structure](common.md))</code><br>
<code>**class** [FindMatchmakeSessionByParticipantParam](#findmatchmakesessionbyparticipantparam)([Structure](common.md))</code><br>
<code>**class** [FindMatchmakeSessionByParticipantResult](#findmatchmakesessionbyparticipantresult)([Structure](common.md))</code><br>
<code>**class** [Gathering](#gathering)([Structure](common.md))</code><br>
<code>**class** [GatheringStats](#gatheringstats)([Structure](common.md))</code><br>
<code>**class** [GatheringURLs](#gatheringurls)([Structure](common.md))</code><br>
<code>**class** [Invitation](#invitation)([Structure](common.md))</code><br>
<code>**class** [JoinMatchmakeSessionParam](#joinmatchmakesessionparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeBlockListParam](#matchmakeblocklistparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeParam](#matchmakeparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeEndRoundParam](#matchmakerefereeendroundparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereePersonalRoundResult](#matchmakerefereepersonalroundresult)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeRound](#matchmakerefereeround)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeStartRoundParam](#matchmakerefereestartroundparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeStats](#matchmakerefereestats)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeStatsInitParam](#matchmakerefereestatsinitparam)([Structure](common.md))</code><br>
<code>**class** [MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)([Structure](common.md))</code><br>
<code>**class** [MatchmakeSession](#matchmakesession)([Gathering](#gathering))</code><br>
<code>**class** [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)([Structure](common.md))</code><br>
<code>**class** [ParticipantDetails](#participantdetails)([Structure](common.md))</code><br>
<code>**class** [PersistentGathering](#persistentgathering)([Gathering](#gathering))</code><br>
<code>**class** [PlayingSession](#playingsession)([Structure](common.md))</code><br>
<code>**class** [SimpleCommunity](#simplecommunity)([Structure](common.md))</code><br>
<code>**class** [SimplePlayingSession](#simpleplayingsession)([Structure](common.md))</code><br>
<code>**class** [UpdateMatchmakeSessionParam](#updatematchmakesessionparam)([Structure](common.md))</code><br>

## MatchMakingClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MatchMakingClient`](#matchmakingclient).</span>

<code>**async def register_gathering**(gathering: [Gathering](#gathering)) -> int</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def unregister_gathering**(gid: int) -> bool</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def unregister_gatherings**(gids: list[int]) -> bool</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def update_gathering**(gathering: [Gathering](#gathering)) -> bool</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def invite**(gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def accept_invitation**(gid: int, message: str) -> bool</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def decline_invitation**(gid: int, message: str) -> bool</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def cancel_invitation**(gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_invitations_sent**(gid: int) -> list[[Invitation](#invitation)]</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def get_invitations_received**() -> list[[Invitation](#invitation)]</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def participate**(gid: int, message: str) -> bool</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def cancel_participation**(gid: int, message: str) -> bool</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def get_participants**(gid: int) -> list[int]</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def add_participants**(gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def get_detailed_participants**(gid: int) -> list[[ParticipantDetails](#participantdetails)]</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def get_participants_urls**(gid: int) -> list[[StationURL](common.md#stationurl)]</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def find_by_type**(type: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def find_by_description**(description: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def find_by_description_regex**(regex: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def find_by_id**(ids: list[int]) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def find_by_single_id**(gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `21` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>gathering: [Gathering](#gathering)</code><br>
</span>
</span>

<code>**async def find_by_owner**(owner: int, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `22` on the server.</span>

<code>**async def find_by_participants**(pids: list[int]) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `23` on the server.</span>

<code>**async def find_invitations**(range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def find_by_sql_query**(query: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def launch_session**(gid: int, url: str) -> bool</code><br>
<span class="docs">Calls method `26` on the server.</span>

<code>**async def update_session_url**(gid: int, url: str) -> bool</code><br>
<span class="docs">Calls method `27` on the server.</span>

<code>**async def get_session_url**(gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `28` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>url: str</code><br>
</span>
</span>

<code>**async def get_state**(gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `29` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>state: int</code><br>
</span>
</span>

<code>**async def set_state**(gid: int, state: int) -> bool</code><br>
<span class="docs">Calls method `30` on the server.</span>

<code>**async def report_stats**(gid: int, stats: list[[GatheringStats](#gatheringstats)]) -> bool</code><br>
<span class="docs">Calls method `31` on the server.</span>

<code>**async def get_stats**(gid: int, pids: list[int], columns: list[int]) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `32` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>stats: list[[GatheringStats](#gatheringstats)]</code><br>
</span>
</span>

<code>**async def delete_gathering**(gid: int) -> bool</code><br>
<span class="docs">Calls method `33` on the server.</span>

<code>**async def get_pending_deletions**(reason: int, range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `34` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>deletions: list[[DeletionEntry](#deletionentry)]</code><br>
</span>
</span>

<code>**async def delete_from_deletions**(deletions: list[int]) -> bool</code><br>
<span class="docs">Calls method `35` on the server.</span>

<code>**async def migrate_gathering_ownership_v1**(gid: int, potential_owners: list[int]) -> bool</code><br>
<span class="docs">Calls method `36` on the server.</span>

<code>**async def find_by_description_like**(description: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `37` on the server.</span>

<code>**async def register_local_url**(gid: int, url: [StationURL](common.md#stationurl)) -> None</code><br>
<span class="docs">Calls method `38` on the server.</span>

<code>**async def register_local_urls**(gid: int, urls: list[[StationURL](common.md#stationurl)]) -> None</code><br>
<span class="docs">Calls method `39` on the server.</span>

<code>**async def update_session_host_v1**(gid: int) -> None</code><br>
<span class="docs">Calls method `40` on the server.</span>

<code>**async def get_session_urls**(gid: int) -> list[[StationURL](common.md#stationurl)]</code><br>
<span class="docs">Calls method `41` on the server.</span>

<code>**async def update_session_host**(gid: int, is_migrate_owner: bool) -> None</code><br>
<span class="docs">Calls method `42` on the server.</span>

<code>**async def update_gathering_ownership**(gid: int, participants_only: bool) -> bool</code><br>
<span class="docs">Calls method `43` on the server.</span>

<code>**async def migrate_gathering_ownership**(gid: int, potential_owners: list[int], participants_only: bool) -> None</code><br>
<span class="docs">Calls method `44` on the server.</span>

## MatchMakingClientExt
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MatchMakingClientExt`](#matchmakingclientext).</span>

<code>**async def end_participation**(gid: int, message: str) -> bool</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def get_participants**(gid: int, only_active: bool) -> list[int]</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def get_detailed_participants**(gid: int, only_active: bool) -> list[[ParticipantDetails](#participantdetails)]</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def get_participants_urls**(gids: list[int]) -> list[[GatheringURLs](#gatheringurls)]</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def get_gathering_relations**(id: int, descr: str) -> str</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def delete_from_deletions**(deletions: list[int], pid: int) -> None</code><br>
<span class="docs">Calls method `6` on the server.</span>

## MatchmakeExtensionClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MatchmakeExtensionClient`](#matchmakeextensionclient).</span>

<code>**async def close_participation**(gid: int) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def open_participation**(gid: int) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def auto_matchmake_postpone**(gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def browse_matchmake_session**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def browse_matchmake_session_with_host_urls**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `5` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>gatherings: list[[Gathering](#gathering)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

<code>**async def create_matchmake_session**(gathering: [Gathering](#gathering), description: str, num_participants: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `6` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>gid: int</code><br>
<code>session_key: bytes</code><br>
</span>
</span>

<code>**async def join_matchmake_session**(gid: int, message: str) -> bytes</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def modify_current_game_attribute**(gid: int, attrib: int, value: int) -> None</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def update_notification_data**(type: int, param1: int, param2: int, param3: str) -> None</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def get_friend_notification_data**(type: int) -> list[[NotificationEvent](notification.md#notificationevent)]</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def update_application_buffer**(gid: int, buffer: bytes) -> None</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def update_matchmake_session_attribute**(gid: int, attribs: list[int]) -> None</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def get_friend_notification_data_list**(types: list[int]) -> list[[NotificationEvent](notification.md#notificationevent)]</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def update_matchmake_session**(gathering: [Gathering](#gathering)) -> None</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def auto_matchmake_with_search_criteria_postpone**(search_criteria: list[[MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)], gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def get_playing_session**(pids: list[int]) -> list[[PlayingSession](#playingsession)]</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def create_community**(community: [PersistentGathering](#persistentgathering), message: str) -> int</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def update_community**(community: [PersistentGathering](#persistentgathering)) -> None</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def join_community**(gid: int, message: str, password: str) -> None</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def find_community_by_gathering_id**(gids: list[int]) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def find_official_community**(available_only: bool, range: [ResultRange](common.md#resultrange)) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Calls method `21` on the server.</span>

<code>**async def find_community_by_participant**(pid: int, range: [ResultRange](common.md#resultrange)) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Calls method `22` on the server.</span>

<code>**async def update_privacy_setting**(online_status: bool, community_participation: bool) -> None</code><br>
<span class="docs">Calls method `23` on the server.</span>

<code>**async def get_my_block_list**() -> list[int]</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def add_to_block_list**(pids: list[int]) -> None</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def remove_from_block_list**(pids: list[int]) -> None</code><br>
<span class="docs">Calls method `26` on the server.</span>

<code>**async def clear_my_block_list**() -> None</code><br>
<span class="docs">Calls method `27` on the server.</span>

<code>**async def report_violation**(pid: int, username: str, violation_code: int) -> None</code><br>
<span class="docs">Calls method `28` on the server.</span>

<code>**async def is_violation_user**() -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `29` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>flag: bool</code><br>
<code>score: int</code><br>
</span>
</span>

<code>**async def join_matchmake_session_ex**(gid: int, gmessage: str, ignore_block_list: bool, num_participants: int) -> bytes</code><br>
<span class="docs">Calls method `30` on the server.</span>

<code>**async def get_simple_playing_session**(pids: list[int], include_login_user: bool) -> list[[SimplePlayingSession](#simpleplayingsession)]</code><br>
<span class="docs">Calls method `31` on the server.</span>

<code>**async def get_simple_community**(gids: list[int]) -> list[[SimpleCommunity](#simplecommunity)]</code><br>
<span class="docs">Calls method `32` on the server.</span>

<code>**async def auto_matchmake_with_gathering_id_postpone**(gids: list[int], gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Calls method `33` on the server.</span>

<code>**async def update_progress_score**(gid: int, score: int) -> None</code><br>
<span class="docs">Calls method `34` on the server.</span>

<code>**async def debug_notify_event**(pid: int, main_type: int, sub_type: int, param1: int, param2: int, param3: str) -> None</code><br>
<span class="docs">Calls method `35` on the server.</span>

<code>**async def generate_matchmake_session_system_password**(gid: int) -> str</code><br>
<span class="docs">Calls method `36` on the server.</span>

<code>**async def clear_matchmake_session_system_password**(gid: int) -> None</code><br>
<span class="docs">Calls method `37` on the server.</span>

<code>**async def create_matchmake_session_with_param**(param: [CreateMatchmakeSessionParam](#creatematchmakesessionparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Calls method `38` on the server.</span>

<code>**async def join_matchmake_session_with_param**(param: [JoinMatchmakeSessionParam](#joinmatchmakesessionparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Calls method `39` on the server.</span>

<code>**async def auto_matchmake_with_param_postpone**(param: [AutoMatchmakeParam](#automatchmakeparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Calls method `40` on the server.</span>

<code>**async def find_matchmake_session_by_gathering_id_detail**(gid: int) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Calls method `41` on the server.</span>

<code>**async def browse_matchmake_session_no_holder**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Calls method `42` on the server.</span>

<code>**async def browse_matchmake_session_with_host_urls_no_holder**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `43` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>sessions: list[[MatchmakeSession](#matchmakesession)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

<code>**async def update_matchmake_session_part**(param: [UpdateMatchmakeSessionParam](#updatematchmakesessionparam)) -> None</code><br>
<span class="docs">Calls method `44` on the server.</span>

<code>**async def request_matchmaking**(param: [AutoMatchmakeParam](#automatchmakeparam)) -> int</code><br>
<span class="docs">Calls method `45` on the server.</span>

<code>**async def withdraw_matchmaking**(request_id: int) -> None</code><br>
<span class="docs">Calls method `46` on the server.</span>

<code>**async def withdraw_matchmaking_all**() -> None</code><br>
<span class="docs">Calls method `47` on the server.</span>

<code>**async def find_matchmake_session_by_gathering_id**(gids: list[int]) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Calls method `48` on the server.</span>

<code>**async def find_matchmake_session_by_single_gathering_id**(gid: int) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Calls method `49` on the server.</span>

<code>**async def find_matchmake_session_by_owner**(pid: int, range: [ResultRange](common.md#resultrange)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Calls method `50` on the server.</span>

<code>**async def find_matchmake_session_by_participant**(param: [FindMatchmakeSessionByParticipantParam](#findmatchmakesessionbyparticipantparam)) -> list[[FindMatchmakeSessionByParticipantResult](#findmatchmakesessionbyparticipantresult)]</code><br>
<span class="docs">Calls method `51` on the server.</span>

<code>**async def browse_matchmake_session_no_holder_no_result_range**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Calls method `52` on the server.</span>

<code>**async def browse_matchmake_session_with_host_urls_no_holder_no_result_range**(search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `53` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>sessions: list[[MatchmakeSession](#matchmakesession)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

## MatchmakeRefereeClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MatchmakeRefereeClient`](#matchmakerefereeclient).</span>

<code>**async def start_round**(param: [MatchmakeRefereeStartRoundParam](#matchmakerefereestartroundparam)) -> int</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def get_start_round_param**(round_id: int) -> [MatchmakeRefereeStartRoundParam](#matchmakerefereestartroundparam)</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def end_round**(param: [MatchmakeRefereeEndRoundParam](#matchmakerefereeendroundparam)) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def end_round_without_report**(round_id: int) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def get_round_participants**(round_id: int) -> list[int]</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_not_summarized_round**() -> list[[MatchmakeRefereeRound](#matchmakerefereeround)]</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def get_round**(round: int) -> [MatchmakeRefereeRound](#matchmakerefereeround)</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def get_stats_primary**(target: [MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_stats_primaries**(targets: list[[MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)]) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `9` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>stats: list[[MatchmakeRefereeStats](#matchmakerefereestats)]</code><br>
<code>results: list[[Result](common.md#result)]</code><br>
</span>
</span>

<code>**async def get_stats_all**(target: [MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)) -> list[[MatchmakeRefereeStats](#matchmakerefereestats)]</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def create_stats**(param: [MatchmakeRefereeStatsInitParam](#matchmakerefereestatsinitparam)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def get_or_create_stats**(param: [MatchmakeRefereeStatsInitParam](#matchmakerefereestatsinitparam)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def reset_stats**() -> None</code><br>
<span class="docs">Calls method `13` on the server.</span>

## MatchMakingServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MatchMakingServer`](#matchmakingserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def register_gathering**(client: [RMCClient](rmc.md#rmcclient), gathering: [Gathering](#gathering)) -> int</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def unregister_gathering**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> bool</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def unregister_gatherings**(client: [RMCClient](rmc.md#rmcclient), gids: list[int]) -> bool</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def update_gathering**(client: [RMCClient](rmc.md#rmcclient), gathering: [Gathering](#gathering)) -> bool</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def invite**(client: [RMCClient](rmc.md#rmcclient), gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def accept_invitation**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bool</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def decline_invitation**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bool</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def cancel_invitation**(client: [RMCClient](rmc.md#rmcclient), gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_invitations_sent**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> list[[Invitation](#invitation)]</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def get_invitations_received**(client: [RMCClient](rmc.md#rmcclient)) -> list[[Invitation](#invitation)]</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def participate**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bool</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def cancel_participation**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bool</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def get_participants**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> list[int]</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def add_participants**(client: [RMCClient](rmc.md#rmcclient), gid: int, pids: list[int], message: str) -> bool</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def get_detailed_participants**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> list[[ParticipantDetails](#participantdetails)]</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def get_participants_urls**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> list[[StationURL](common.md#stationurl)]</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def find_by_type**(client: [RMCClient](rmc.md#rmcclient), type: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def find_by_description**(client: [RMCClient](rmc.md#rmcclient), description: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def find_by_description_regex**(client: [RMCClient](rmc.md#rmcclient), regex: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def find_by_id**(client: [RMCClient](rmc.md#rmcclient), ids: list[int]) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def find_by_single_id**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `21`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>gathering: [Gathering](#gathering)</code><br>
</span>
</span>

<code>**async def find_by_owner**(client: [RMCClient](rmc.md#rmcclient), owner: int, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

<code>**async def find_by_participants**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `23`. This method should be overridden by a subclass.</span>

<code>**async def find_invitations**(client: [RMCClient](rmc.md#rmcclient), range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def find_by_sql_query**(client: [RMCClient](rmc.md#rmcclient), query: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def launch_session**(client: [RMCClient](rmc.md#rmcclient), gid: int, url: str) -> bool</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

<code>**async def update_session_url**(client: [RMCClient](rmc.md#rmcclient), gid: int, url: str) -> bool</code><br>
<span class="docs">Handler for method `27`. This method should be overridden by a subclass.</span>

<code>**async def get_session_url**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `28`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>url: str</code><br>
</span>
</span>

<code>**async def get_state**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `29`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>state: int</code><br>
</span>
</span>

<code>**async def set_state**(client: [RMCClient](rmc.md#rmcclient), gid: int, state: int) -> bool</code><br>
<span class="docs">Handler for method `30`. This method should be overridden by a subclass.</span>

<code>**async def report_stats**(client: [RMCClient](rmc.md#rmcclient), gid: int, stats: list[[GatheringStats](#gatheringstats)]) -> bool</code><br>
<span class="docs">Handler for method `31`. This method should be overridden by a subclass.</span>

<code>**async def get_stats**(client: [RMCClient](rmc.md#rmcclient), gid: int, pids: list[int], columns: list[int]) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `32`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>stats: list[[GatheringStats](#gatheringstats)]</code><br>
</span>
</span>

<code>**async def delete_gathering**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> bool</code><br>
<span class="docs">Handler for method `33`. This method should be overridden by a subclass.</span>

<code>**async def get_pending_deletions**(client: [RMCClient](rmc.md#rmcclient), reason: int, range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `34`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>deletions: list[[DeletionEntry](#deletionentry)]</code><br>
</span>
</span>

<code>**async def delete_from_deletions**(client: [RMCClient](rmc.md#rmcclient), deletions: list[int]) -> bool</code><br>
<span class="docs">Handler for method `35`. This method should be overridden by a subclass.</span>

<code>**async def migrate_gathering_ownership_v1**(client: [RMCClient](rmc.md#rmcclient), gid: int, potential_owners: list[int]) -> bool</code><br>
<span class="docs">Handler for method `36`. This method should be overridden by a subclass.</span>

<code>**async def find_by_description_like**(client: [RMCClient](rmc.md#rmcclient), description: str, range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `37`. This method should be overridden by a subclass.</span>

<code>**async def register_local_url**(client: [RMCClient](rmc.md#rmcclient), gid: int, url: [StationURL](common.md#stationurl)) -> None</code><br>
<span class="docs">Handler for method `38`. This method should be overridden by a subclass.</span>

<code>**async def register_local_urls**(client: [RMCClient](rmc.md#rmcclient), gid: int, urls: list[[StationURL](common.md#stationurl)]) -> None</code><br>
<span class="docs">Handler for method `39`. This method should be overridden by a subclass.</span>

<code>**async def update_session_host_v1**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> None</code><br>
<span class="docs">Handler for method `40`. This method should be overridden by a subclass.</span>

<code>**async def get_session_urls**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> list[[StationURL](common.md#stationurl)]</code><br>
<span class="docs">Handler for method `41`. This method should be overridden by a subclass.</span>

<code>**async def update_session_host**(client: [RMCClient](rmc.md#rmcclient), gid: int, is_migrate_owner: bool) -> None</code><br>
<span class="docs">Handler for method `42`. This method should be overridden by a subclass.</span>

<code>**async def update_gathering_ownership**(client: [RMCClient](rmc.md#rmcclient), gid: int, participants_only: bool) -> bool</code><br>
<span class="docs">Handler for method `43`. This method should be overridden by a subclass.</span>

<code>**async def migrate_gathering_ownership**(client: [RMCClient](rmc.md#rmcclient), gid: int, potential_owners: list[int], participants_only: bool) -> None</code><br>
<span class="docs">Handler for method `44`. This method should be overridden by a subclass.</span>

## MatchMakingServerExt
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MatchMakingServerExt`](#matchmakingserverext).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def end_participation**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bool</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def get_participants**(client: [RMCClient](rmc.md#rmcclient), gid: int, only_active: bool) -> list[int]</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def get_detailed_participants**(client: [RMCClient](rmc.md#rmcclient), gid: int, only_active: bool) -> list[[ParticipantDetails](#participantdetails)]</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def get_participants_urls**(client: [RMCClient](rmc.md#rmcclient), gids: list[int]) -> list[[GatheringURLs](#gatheringurls)]</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def get_gathering_relations**(client: [RMCClient](rmc.md#rmcclient), id: int, descr: str) -> str</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def delete_from_deletions**(client: [RMCClient](rmc.md#rmcclient), deletions: list[int], pid: int) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

## MatchmakeExtensionServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MatchmakeExtensionServer`](#matchmakeextensionserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def close_participation**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def open_participation**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def auto_matchmake_postpone**(client: [RMCClient](rmc.md#rmcclient), gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> list[[Gathering](#gathering)]</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session_with_host_urls**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>gatherings: list[[Gathering](#gathering)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

<code>**async def create_matchmake_session**(client: [RMCClient](rmc.md#rmcclient), gathering: [Gathering](#gathering), description: str, num_participants: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>gid: int</code><br>
<code>session_key: bytes</code><br>
</span>
</span>

<code>**async def join_matchmake_session**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str) -> bytes</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def modify_current_game_attribute**(client: [RMCClient](rmc.md#rmcclient), gid: int, attrib: int, value: int) -> None</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def update_notification_data**(client: [RMCClient](rmc.md#rmcclient), type: int, param1: int, param2: int, param3: str) -> None</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_notification_data**(client: [RMCClient](rmc.md#rmcclient), type: int) -> list[[NotificationEvent](notification.md#notificationevent)]</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def update_application_buffer**(client: [RMCClient](rmc.md#rmcclient), gid: int, buffer: bytes) -> None</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def update_matchmake_session_attribute**(client: [RMCClient](rmc.md#rmcclient), gid: int, attribs: list[int]) -> None</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_notification_data_list**(client: [RMCClient](rmc.md#rmcclient), types: list[int]) -> list[[NotificationEvent](notification.md#notificationevent)]</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def update_matchmake_session**(client: [RMCClient](rmc.md#rmcclient), gathering: [Gathering](#gathering)) -> None</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def auto_matchmake_with_search_criteria_postpone**(client: [RMCClient](rmc.md#rmcclient), search_criteria: list[[MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)], gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def get_playing_session**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> list[[PlayingSession](#playingsession)]</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def create_community**(client: [RMCClient](rmc.md#rmcclient), community: [PersistentGathering](#persistentgathering), message: str) -> int</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def update_community**(client: [RMCClient](rmc.md#rmcclient), community: [PersistentGathering](#persistentgathering)) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def join_community**(client: [RMCClient](rmc.md#rmcclient), gid: int, message: str, password: str) -> None</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def find_community_by_gathering_id**(client: [RMCClient](rmc.md#rmcclient), gids: list[int]) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def find_official_community**(client: [RMCClient](rmc.md#rmcclient), available_only: bool, range: [ResultRange](common.md#resultrange)) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Handler for method `21`. This method should be overridden by a subclass.</span>

<code>**async def find_community_by_participant**(client: [RMCClient](rmc.md#rmcclient), pid: int, range: [ResultRange](common.md#resultrange)) -> list[[PersistentGathering](#persistentgathering)]</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

<code>**async def update_privacy_setting**(client: [RMCClient](rmc.md#rmcclient), online_status: bool, community_participation: bool) -> None</code><br>
<span class="docs">Handler for method `23`. This method should be overridden by a subclass.</span>

<code>**async def get_my_block_list**(client: [RMCClient](rmc.md#rmcclient)) -> list[int]</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def add_to_block_list**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> None</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def remove_from_block_list**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> None</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

<code>**async def clear_my_block_list**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `27`. This method should be overridden by a subclass.</span>

<code>**async def report_violation**(client: [RMCClient](rmc.md#rmcclient), pid: int, username: str, violation_code: int) -> None</code><br>
<span class="docs">Handler for method `28`. This method should be overridden by a subclass.</span>

<code>**async def is_violation_user**(client: [RMCClient](rmc.md#rmcclient)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `29`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>flag: bool</code><br>
<code>score: int</code><br>
</span>
</span>

<code>**async def join_matchmake_session_ex**(client: [RMCClient](rmc.md#rmcclient), gid: int, gmessage: str, ignore_block_list: bool, num_participants: int) -> bytes</code><br>
<span class="docs">Handler for method `30`. This method should be overridden by a subclass.</span>

<code>**async def get_simple_playing_session**(client: [RMCClient](rmc.md#rmcclient), pids: list[int], include_login_user: bool) -> list[[SimplePlayingSession](#simpleplayingsession)]</code><br>
<span class="docs">Handler for method `31`. This method should be overridden by a subclass.</span>

<code>**async def get_simple_community**(client: [RMCClient](rmc.md#rmcclient), gids: list[int]) -> list[[SimpleCommunity](#simplecommunity)]</code><br>
<span class="docs">Handler for method `32`. This method should be overridden by a subclass.</span>

<code>**async def auto_matchmake_with_gathering_id_postpone**(client: [RMCClient](rmc.md#rmcclient), gids: list[int], gathering: [Gathering](#gathering), message: str) -> [Gathering](#gathering)</code><br>
<span class="docs">Handler for method `33`. This method should be overridden by a subclass.</span>

<code>**async def update_progress_score**(client: [RMCClient](rmc.md#rmcclient), gid: int, score: int) -> None</code><br>
<span class="docs">Handler for method `34`. This method should be overridden by a subclass.</span>

<code>**async def debug_notify_event**(client: [RMCClient](rmc.md#rmcclient), pid: int, main_type: int, sub_type: int, param1: int, param2: int, param3: str) -> None</code><br>
<span class="docs">Handler for method `35`. This method should be overridden by a subclass.</span>

<code>**async def generate_matchmake_session_system_password**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> str</code><br>
<span class="docs">Handler for method `36`. This method should be overridden by a subclass.</span>

<code>**async def clear_matchmake_session_system_password**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> None</code><br>
<span class="docs">Handler for method `37`. This method should be overridden by a subclass.</span>

<code>**async def create_matchmake_session_with_param**(client: [RMCClient](rmc.md#rmcclient), param: [CreateMatchmakeSessionParam](#creatematchmakesessionparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Handler for method `38`. This method should be overridden by a subclass.</span>

<code>**async def join_matchmake_session_with_param**(client: [RMCClient](rmc.md#rmcclient), param: [JoinMatchmakeSessionParam](#joinmatchmakesessionparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Handler for method `39`. This method should be overridden by a subclass.</span>

<code>**async def auto_matchmake_with_param_postpone**(client: [RMCClient](rmc.md#rmcclient), param: [AutoMatchmakeParam](#automatchmakeparam)) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Handler for method `40`. This method should be overridden by a subclass.</span>

<code>**async def find_matchmake_session_by_gathering_id_detail**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Handler for method `41`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session_no_holder**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Handler for method `42`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session_with_host_urls_no_holder**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria), range: [ResultRange](common.md#resultrange)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `43`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>sessions: list[[MatchmakeSession](#matchmakesession)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

<code>**async def update_matchmake_session_part**(client: [RMCClient](rmc.md#rmcclient), param: [UpdateMatchmakeSessionParam](#updatematchmakesessionparam)) -> None</code><br>
<span class="docs">Handler for method `44`. This method should be overridden by a subclass.</span>

<code>**async def request_matchmaking**(client: [RMCClient](rmc.md#rmcclient), param: [AutoMatchmakeParam](#automatchmakeparam)) -> int</code><br>
<span class="docs">Handler for method `45`. This method should be overridden by a subclass.</span>

<code>**async def withdraw_matchmaking**(client: [RMCClient](rmc.md#rmcclient), request_id: int) -> None</code><br>
<span class="docs">Handler for method `46`. This method should be overridden by a subclass.</span>

<code>**async def withdraw_matchmaking_all**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `47`. This method should be overridden by a subclass.</span>

<code>**async def find_matchmake_session_by_gathering_id**(client: [RMCClient](rmc.md#rmcclient), gids: list[int]) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Handler for method `48`. This method should be overridden by a subclass.</span>

<code>**async def find_matchmake_session_by_single_gathering_id**(client: [RMCClient](rmc.md#rmcclient), gid: int) -> [MatchmakeSession](#matchmakesession)</code><br>
<span class="docs">Handler for method `49`. This method should be overridden by a subclass.</span>

<code>**async def find_matchmake_session_by_owner**(client: [RMCClient](rmc.md#rmcclient), pid: int, range: [ResultRange](common.md#resultrange)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Handler for method `50`. This method should be overridden by a subclass.</span>

<code>**async def find_matchmake_session_by_participant**(client: [RMCClient](rmc.md#rmcclient), param: [FindMatchmakeSessionByParticipantParam](#findmatchmakesessionbyparticipantparam)) -> list[[FindMatchmakeSessionByParticipantResult](#findmatchmakesessionbyparticipantresult)]</code><br>
<span class="docs">Handler for method `51`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session_no_holder_no_result_range**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)) -> list[[MatchmakeSession](#matchmakesession)]</code><br>
<span class="docs">Handler for method `52`. This method should be overridden by a subclass.</span>

<code>**async def browse_matchmake_session_with_host_urls_no_holder_no_result_range**(client: [RMCClient](rmc.md#rmcclient), search_criteria: [MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `53`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>sessions: list[[MatchmakeSession](#matchmakesession)]</code><br>
<code>urls: list[[GatheringURLs](#gatheringurls)]</code><br>
</span>
</span>

## MatchmakeRefereeServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MatchmakeRefereeServer`](#matchmakerefereeserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def start_round**(client: [RMCClient](rmc.md#rmcclient), param: [MatchmakeRefereeStartRoundParam](#matchmakerefereestartroundparam)) -> int</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def get_start_round_param**(client: [RMCClient](rmc.md#rmcclient), round_id: int) -> [MatchmakeRefereeStartRoundParam](#matchmakerefereestartroundparam)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def end_round**(client: [RMCClient](rmc.md#rmcclient), param: [MatchmakeRefereeEndRoundParam](#matchmakerefereeendroundparam)) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def end_round_without_report**(client: [RMCClient](rmc.md#rmcclient), round_id: int) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def get_round_participants**(client: [RMCClient](rmc.md#rmcclient), round_id: int) -> list[int]</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_not_summarized_round**(client: [RMCClient](rmc.md#rmcclient)) -> list[[MatchmakeRefereeRound](#matchmakerefereeround)]</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def get_round**(client: [RMCClient](rmc.md#rmcclient), round: int) -> [MatchmakeRefereeRound](#matchmakerefereeround)</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def get_stats_primary**(client: [RMCClient](rmc.md#rmcclient), target: [MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_stats_primaries**(client: [RMCClient](rmc.md#rmcclient), targets: list[[MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)]) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>stats: list[[MatchmakeRefereeStats](#matchmakerefereestats)]</code><br>
<code>results: list[[Result](common.md#result)]</code><br>
</span>
</span>

<code>**async def get_stats_all**(client: [RMCClient](rmc.md#rmcclient), target: [MatchmakeRefereeStatsTarget](#matchmakerefereestatstarget)) -> list[[MatchmakeRefereeStats](#matchmakerefereestats)]</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def create_stats**(client: [RMCClient](rmc.md#rmcclient), param: [MatchmakeRefereeStatsInitParam](#matchmakerefereestatsinitparam)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def get_or_create_stats**(client: [RMCClient](rmc.md#rmcclient), param: [MatchmakeRefereeStatsInitParam](#matchmakerefereestatsinitparam)) -> [MatchmakeRefereeStats](#matchmakerefereestats)</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def reset_stats**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

## MatchmakeSystem
This class defines the following constants:<br>
<span class="docs">
`GLOBAL = 1`<br>
`FRIENDS = 2`<br>
</span>

## AutoMatchmakeParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `AutoMatchmakeParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>session: [MatchmakeSession](#matchmakesession) = [MatchmakeSession](#matchmakesession)()</code><br>
<code>participants: list[int]</code><br>
<code>gid_for_participation_check: int</code><br>
<code>options: int</code><br>
<code>join_message: str</code><br>
<code>num_participants: int</code><br>
<code>search_criteria: list[[MatchmakeSessionSearchCriteria](#matchmakesessionsearchcriteria)]</code><br>
<code>target_gids: list[int]</code><br>
<code>block_list: [MatchmakeBlockListParam](#matchmakeblocklistparam) = [MatchmakeBlockListParam](#matchmakeblocklistparam)()</code><br>
</span><br>

## CreateMatchmakeSessionParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `CreateMatchmakeSessionParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>session: [MatchmakeSession](#matchmakesession) = [MatchmakeSession](#matchmakesession)()</code><br>
<code>additional_participants: list[int]</code><br>
<code>gid_for_participation_check: int</code><br>
<code>options: int</code><br>
<code>join_message: str</code><br>
<code>num_participants: int</code><br>
</span><br>

## DeletionEntry
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DeletionEntry` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>pid: int</code><br>
<code>reason: int</code><br>
</span><br>

## FindMatchmakeSessionByParticipantParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FindMatchmakeSessionByParticipantParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pids: list[int]</code><br>
<code>options: int</code><br>
<code>block_list: [MatchmakeBlockListParam](#matchmakeblocklistparam) = [MatchmakeBlockListParam](#matchmakeblocklistparam)()</code><br>
</span><br>

## FindMatchmakeSessionByParticipantResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FindMatchmakeSessionByParticipantResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>session: [MatchmakeSession](#matchmakesession) = [MatchmakeSession](#matchmakesession)()</code><br>
</span><br>

## Gathering
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Gathering` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>id: int = 0</code><br>
<code>owner: int = 0</code><br>
<code>host: int = 0</code><br>
<code>min_participants: int = 0</code><br>
<code>max_participants: int = 0</code><br>
<code>participation_policy: int = 1</code><br>
<code>policy_argument: int = 0</code><br>
<code>flags: int = 512</code><br>
<code>state: int = 0</code><br>
<code>description: str = ""</code><br>
</span><br>

## GatheringStats
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `GatheringStats` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>flags: int</code><br>
<code>values: list[float]</code><br>
</span><br>

## GatheringURLs
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `GatheringURLs` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>urls: list[[StationURL](common.md#stationurl)]</code><br>
</span><br>

## Invitation
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Invitation` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>guest: int</code><br>
<code>message: str</code><br>
</span><br>

## JoinMatchmakeSessionParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `JoinMatchmakeSessionParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>participants: list[int]</code><br>
<code>gid_for_participation_check: int</code><br>
<code>options: int</code><br>
<code>behavior: int</code><br>
<code>user_password: str</code><br>
<code>system_password: str</code><br>
<code>join_message: str</code><br>
<code>num_participants: int</code><br>
<code>extra_participants: int</code><br>
<code>block_list: [MatchmakeBlockListParam](#matchmakeblocklistparam) = [MatchmakeBlockListParam](#matchmakeblocklistparam)()</code><br>
</span><br>

## MatchmakeBlockListParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeBlockListParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>options: int = 0</code><br>
</span><br>

## MatchmakeParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>param: dict[str, object] = {}</code><br>
</span><br>

## MatchmakeRefereeEndRoundParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeEndRoundParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>round_id: int</code><br>
<code>results: list[[MatchmakeRefereePersonalRoundResult](#matchmakerefereepersonalroundresult)]</code><br>
</span><br>

## MatchmakeRefereePersonalRoundResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereePersonalRoundResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>personal_round_result_flag: int</code><br>
<code>round_win_loss: int</code><br>
<code>rating_change: int</code><br>
<code>buffer: bytes</code><br>
</span><br>

## MatchmakeRefereeRound
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeRound` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>id: int</code><br>
<code>gid: int</code><br>
<code>state: int</code><br>
<code>personal_data_category: int</code><br>
<code>results: list[[MatchmakeRefereePersonalRoundResult](#matchmakerefereepersonalroundresult)]</code><br>
</span><br>

## MatchmakeRefereeStartRoundParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeStartRoundParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>personal_data_category: int</code><br>
<code>gid: int</code><br>
<code>pids: list[int]</code><br>
</span><br>

## MatchmakeRefereeStats
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeStats` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unique_id: int</code><br>
<code>category: int</code><br>
<code>pid: int</code><br>
<code>recent_disconnection: int</code><br>
<code>recent_violation: int</code><br>
<code>recent_mismatch: int</code><br>
<code>recent_win: int</code><br>
<code>recent_loss: int</code><br>
<code>recent_draw: int</code><br>
<code>total_disconnect: int</code><br>
<code>total_violation: int</code><br>
<code>total_mismatch: int</code><br>
<code>total_win: int</code><br>
<code>total_loss: int</code><br>
<code>total_draw: int</code><br>
<code>rating_value: int</code><br>
</span><br>

## MatchmakeRefereeStatsInitParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeStatsInitParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>category: int</code><br>
<code>initial_rating: int</code><br>
</span><br>

## MatchmakeRefereeStatsTarget
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeRefereeStatsTarget` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>category: int</code><br>
</span><br>

## MatchmakeSession
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeSession` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>game_mode: int = 0</code><br>
<code>attribs: list[int] = [0, 0, 0, 0, 0, 0]</code><br>
<code>open_participation: bool = True</code><br>
<code>matchmake_system: int = 0</code><br>
<code>application_data: bytes = b""</code><br>
<code>num_participants: int = 0</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>progress_score: int = 100</code><br>
</span><br>
If `nex.version` >= 30000:<br>
<span class="docs">
<code>session_key: bytes = b""</code><br>
</span><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>option: int = 0</code><br>
</span><br>
If `nex.version` >= 30600:<br>
<span class="docs">
If `revision` >= 1:<br>
<span class="docs">
<code>param: [MatchmakeParam](#matchmakeparam) = [MatchmakeParam](#matchmakeparam)()</code><br>
<code>started_time: [DateTime](common.md#datetime) = [DateTime](common.md#datetime).never()</code><br>
</span><br>
</span><br>
If `nex.version` >= 30700:<br>
<span class="docs">
If `revision` >= 2:<br>
<span class="docs">
<code>user_password: str = ""</code><br>
</span><br>
</span><br>
If `nex.version` >= 30800:<br>
<span class="docs">
If `revision` >= 3:<br>
<span class="docs">
<code>refer_gid: int = 0</code><br>
<code>user_password_enabled: bool = False</code><br>
<code>system_password_enabled: bool = False</code><br>
</span><br>
</span><br>
If `nex.version` >= 40000:<br>
<span class="docs">
If `revision` >= 0:<br>
<span class="docs">
<code>codeword: str = ""</code><br>
</span><br>
</span><br>
</span><br>

## MatchmakeSessionSearchCriteria
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MatchmakeSessionSearchCriteria` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>attribs: list[str] = ["", "", "", "", "", ""]</code><br>
<code>game_mode: str = ""</code><br>
<code>min_participants: str = ""</code><br>
<code>max_participants: str = ""</code><br>
<code>matchmake_system: str = ""</code><br>
<code>vacant_only: bool = True</code><br>
<code>exclude_locked: bool = True</code><br>
<code>exclude_non_host_pid: bool = False</code><br>
<code>selection_method: int = 0</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>vacant_participants: int = 1</code><br>
</span><br>
If `nex.version` >= 40000:<br>
<span class="docs">
<code>param: [MatchmakeParam](#matchmakeparam) = [MatchmakeParam](#matchmakeparam)()</code><br>
<code>exclude_user_password: bool = False</code><br>
<code>exclude_system_password: bool = False</code><br>
<code>refer_gid: int = 0</code><br>
<code>codeword: str = ""</code><br>
<code>range: [ResultRange](common.md#resultrange) = [ResultRange](common.md#resultrange)()</code><br>
</span><br>
</span><br>

## ParticipantDetails
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ParticipantDetails` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>name: str</code><br>
<code>message: str</code><br>
<code>participants: int</code><br>
</span><br>

## PersistentGathering
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PersistentGathering` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>type: int</code><br>
<code>password: str</code><br>
<code>attribs: list[int]</code><br>
<code>application_buffer: bytes</code><br>
<code>participation_start: [DateTime](common.md#datetime)</code><br>
<code>participation_end: [DateTime](common.md#datetime)</code><br>
<code>matchmake_session_count: int</code><br>
<code>num_participants: int</code><br>
</span><br>

## PlayingSession
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PlayingSession` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>gathering: [Gathering](#gathering)</code><br>
</span><br>

## SimpleCommunity
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `SimpleCommunity` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>matchmake_session_count: int</code><br>
</span><br>

## SimplePlayingSession
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `SimplePlayingSession` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>gid: int</code><br>
<code>game_mode: int</code><br>
<code>attribute: int</code><br>
</span><br>

## UpdateMatchmakeSessionParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `UpdateMatchmakeSessionParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>gid: int</code><br>
<code>modification_flags: int</code><br>
<code>attributes: list[int]</code><br>
<code>open_participation: bool</code><br>
<code>application_buffer: bytes</code><br>
<code>progress_score: int</code><br>
<code>param: [MatchmakeParam](#matchmakeparam) = [MatchmakeParam](#matchmakeparam)()</code><br>
<code>started_time: [DateTime](common.md#datetime)</code><br>
<code>user_password: str</code><br>
<code>game_mode: int</code><br>
<code>description: str</code><br>
<code>min_participants: int</code><br>
<code>max_participants: int</code><br>
<code>matchmake_system: int</code><br>
<code>participation_policy: int</code><br>
<code>policy_argument: int</code><br>
<code>codeword: str</code><br>
</span><br>

