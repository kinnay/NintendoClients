
# Module: <code>nintendo.nex.nattraversal</code>

Provides a client and server for the `NATTraversalProtocol`. This page was generated automatically from `nattraversal.proto`.

<code>**class** [NATTraversalClient](#nattraversalclient)</code><br>
<span class="docs">The client for the `NATTraversalProtocol`.</span>

<code>**class** [NATTraversalServer](#nattraversalserver)</code><br>
<span class="docs">The server for the `NATTraversalProtocol`.</span>

## NATTraversalClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`NATTraversalClient`](#nattraversalclient).</span>

<code>**async def request_probe_initiation**(target_urls: list[[StationURL](../common#stationurl)]) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def initiate_probe**(station_to_probe: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def request_probe_initiation_ext**(target_urls: list[[StationURL](../common#stationurl)], station_to_probe: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def report_nat_traversal_result**(cid: int, result: bool) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def report_nat_properties**(natm: int, natf: int, rtt: int) -> None</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_relay_signature_key**() -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `6` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>mode: int</code><br>
<code>time: [DateTime](../common#datetime)</code><br>
<code>address: str</code><br>
<code>port: int</code><br>
<code>address_type: int</code><br>
<code>game_server_id: int</code><br>
</span>
</span>

<code>**async def report_nat_traversal_result_detail**(cid: int, result: bool, detail: int, rtt: int) -> None</code><br>
<span class="docs">Calls method `7` on the server.</span>

## NATTraversalServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`NATTraversalServer`](#nattraversalserver).</span>

<code>**async def logout**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def request_probe_initiation**(client: [RMCClient](../rmc#rmcclient), target_urls: list[[StationURL](../common#stationurl)]) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def initiate_probe**(client: [RMCClient](../rmc#rmcclient), station_to_probe: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def request_probe_initiation_ext**(client: [RMCClient](../rmc#rmcclient), target_urls: list[[StationURL](../common#stationurl)], station_to_probe: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def report_nat_traversal_result**(client: [RMCClient](../rmc#rmcclient), cid: int, result: bool) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def report_nat_properties**(client: [RMCClient](../rmc#rmcclient), natm: int, natf: int, rtt: int) -> None</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_relay_signature_key**(client: [RMCClient](../rmc#rmcclient)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>mode: int</code><br>
<code>time: [DateTime](../common#datetime)</code><br>
<code>address: str</code><br>
<code>port: int</code><br>
<code>address_type: int</code><br>
<code>game_server_id: int</code><br>
</span>
</span>

<code>**async def report_nat_traversal_result_detail**(client: [RMCClient](../rmc#rmcclient), cid: int, result: bool, detail: int, rtt: int) -> None</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

