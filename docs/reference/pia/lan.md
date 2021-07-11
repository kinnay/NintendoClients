
# Module: <code>nintendo.pia.lan</code>

Provides a client that can search for LAN sessions on the wifi network.

<code>**class** [LanSessionSearchCriteria](#lansessionsearchcriteria)</code><br>
<span class="docs">Search criteria for LAN session discovery.</span>

<code>**class** [LanSessionInfo](#lansessioninfo)</code><br>
<span class="docs">Information about a LAN session.</span>

<code>**class** [LanStationInfo](#lanstationinfo)</code><br>
<span class="docs">Information about a station in a LAN session.</span>

<code>**async def browse**(settings: [Settings](settings.md#settings), search_criteria: [LanSessionSearchCriteria](#lansessionsearchcriteria), key: bytes = None, timeout: float = 1, max: int = 0) -> list[[LanSessionInfo](#lansessioninfo)]</code><br>
<span class="docs">Searches for LAN sessions that match the given search criteria. Blocks until either `max` different LAN session are discovered or the `timeout` has expired. If `max` is `0`, this function always keeps listening until the timeout expires.</span>

<code>**async with serve**(settings: [Settings](settings.md#settings), handler: Callable, key: bytes = None) -> None</code><br>
<span class="docs">Hosts a server that replies to browse requests. `handler` should be a function that takes no arguments and returns the list of active [`LanSessionInfo`](#lansessioninfo) objects.</span>

## LanSessionSearchCriteria
<code>min_participants: [Range](types.md#range) = None</code><br>
<span class="docs">Specifies the allowed range of values for the minimum number of participants.</span>

<code>max_participants: [Range](types.md#range) = None</code><br>
<span class="docs">Specifies the allowed range of values for the minimum number of participants.</span>

`opened_only: bool = None`<br>
<span class="docs">If `True`, only sessions that are opened for participation are returned.</span>

`vacant_only: bool = None`<br>
<span class="docs">If `True`, only sessions with less than the maximum number of participants are returned.</span>

<code>result_range: [ResultRange](types.md#resultrange) = [ResultRange](types.md#resultrange)()</code><br>
<span class="docs">Result range. This controls which LAN sessions are returned if multiple LAN sessions match the given search criteria on a single host. This attribute seems to be ignored by real consoles, since they never host more than one LAN session at once.</span>

`game_mode: int = None`<br>
<span class="docs">If set, only sessions with the specified game mode are returned.</span>

`session_type: int = None`<br>
<span class="docs">If set, only sessions with the specified session type are returned.</span>

`attributes: list = [None] * 6`<br>
<span class="docs">Only sessions with the given attributes are returned. Every item should either be a [`Range`](types.md#range) object or a `list[int]` of accepted values.</span>

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [LanSessionSearchCriteria](#lansessionsearchcriteria) object with no restrictions.</span>

<code>**def reset**()</code><br>
<span class="docs">Resets the search criteria.</span>

<code>**def check**(session_info: [LanSessionInfo](#lansessioninfo)) -> bool</code><br>
<span class="docs">Checks if the search criteria match the given session info.</span>

## LanSessionInfo
`game_mode: int`<br>
`session_id: int`<br>
`attributes: list[int]`<br>
`num_participants: int`<br>
`min_participants: int`<br>
`max_participants: int`<br>
`system_version: int`<br>
`application_version: int`<br>
`session_type: int`<br>
`application_data: bytes`<br>
`is_opened: bool`<br>
<code>host_location: [StationLocation](types.md#stationlocation)</code><br>
<code>stations: list[[LanStationInfo](#lanstationinfo)]</code><br>
`session_param: bytes`

## LanStationInfo
Roles:<br>
<span class="docs">
`HOST = 1`<br>
`PLAYER = 2`<br>
</span>

`role: int`<br>
`username: str`<br>
`id: int`
