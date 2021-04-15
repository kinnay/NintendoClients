
# Module: <code>nintendo.nex.secure</code>

Provides a client and server for the `SecureConnectionProtocol`. This page was generated automatically from `secure.proto`.

<code>**class** [SecureConnectionClient](#secureconnectionclient)</code><br>
<span class="docs">The client for the `SecureConnectionProtocol`.</span>

<code>**class** [SecureConnectionServer](#secureconnectionserver)</code><br>
<span class="docs">The server for the `SecureConnectionProtocol`.</span>

<code>**class** [ConnectionData](#connectiondata)([Structure](../common))</code><br>
<code>**class** [NintendoLoginData](#nintendologindata)([Structure](../common))</code><br>

## SecureConnectionClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`SecureConnectionClient`](#secureconnectionclient).</span>

<code>**async def register**(urls: list[[StationURL](../common#stationurl)]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `1` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>connection_id: int</code><br>
<code>public_station: [StationURL](../common#stationurl)</code><br>
</span>
</span>

<code>**async def request_connection_data**(cid: int, pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `2` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>connection_data: list[[ConnectionData](#connectiondata)]</code><br>
</span>
</span>

<code>**async def request_urls**(cid: int, pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `3` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>urls: list[[StationURL](../common#stationurl)]</code><br>
</span>
</span>

<code>**async def register_ex**(urls: list[[StationURL](../common#stationurl)], login_data: [Data](../common)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `4` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>connection_id: int</code><br>
<code>public_station: [StationURL](../common#stationurl)</code><br>
</span>
</span>

<code>**async def test_connectivity**() -> None</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def replace_url**(url: [StationURL](../common#stationurl), new: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def send_report**(report_id: int, data: bytes) -> None</code><br>
<span class="docs">Calls method `7` on the server.</span>

## SecureConnectionServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`SecureConnectionServer`](#secureconnectionserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def register**(client: [RMCClient](../rmc#rmcclient), urls: list[[StationURL](../common#stationurl)]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>connection_id: int</code><br>
<code>public_station: [StationURL](../common#stationurl)</code><br>
</span>
</span>

<code>**async def request_connection_data**(client: [RMCClient](../rmc#rmcclient), cid: int, pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>connection_data: list[[ConnectionData](#connectiondata)]</code><br>
</span>
</span>

<code>**async def request_urls**(client: [RMCClient](../rmc#rmcclient), cid: int, pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>urls: list[[StationURL](../common#stationurl)]</code><br>
</span>
</span>

<code>**async def register_ex**(client: [RMCClient](../rmc#rmcclient), urls: list[[StationURL](../common#stationurl)], login_data: [Data](../common)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>connection_id: int</code><br>
<code>public_station: [StationURL](../common#stationurl)</code><br>
</span>
</span>

<code>**async def test_connectivity**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def replace_url**(client: [RMCClient](../rmc#rmcclient), url: [StationURL](../common#stationurl), new: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def send_report**(client: [RMCClient](../rmc#rmcclient), report_id: int, data: bytes) -> None</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

## ConnectionData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ConnectionData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>station: [StationURL](../common#stationurl)</code><br>
<code>connection_id: int</code><br>
</span><br>

## NintendoLoginData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoLoginData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>token: str</code><br>
</span><br>

