
# Module: <code>nintendo.nex.authentication</code>

Provides a client and server for the `AuthenticationProtocol` and `AuthenticationProtocolNX`. This page was generated automatically from `authentication.proto`.

<code>**class** [AuthenticationClient](#authenticationclient)</code><br>
<span class="docs">The client for the `AuthenticationProtocol`.</span>

<code>**class** [AuthenticationClientNX](#authenticationclientnx)</code><br>
<span class="docs">The client for the `AuthenticationProtocolNX`.</span>

<code>**class** [AuthenticationServer](#authenticationserver)</code><br>
<span class="docs">The server for the `AuthenticationProtocol`.</span>

<code>**class** [AuthenticationServerNX](#authenticationservernx)</code><br>
<span class="docs">The server for the `AuthenticationProtocolNX`.</span>

<code>**class** [AuthenticationInfo](#authenticationinfo)([Data](common.md))</code><br>
<code>**class** [RVConnectionData](#rvconnectiondata)([Structure](common.md))</code><br>
<code>**class** [ValidateAndRequestTicketParam](#validateandrequestticketparam)([Structure](common.md))</code><br>
<code>**class** [ValidateAndRequestTicketResult](#validateandrequestticketresult)([Structure](common.md))</code><br>

## AuthenticationClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`AuthenticationClient`](#authenticationclient).</span>

<code>**async def login**(username: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `1` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def login_ex**(username: str, extra_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `2` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def request_ticket**(source: int, target: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `3` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>ticket: bytes</code><br>
</span>
</span>

<code>**async def get_pid**(username: str) -> int</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def get_name**(pid: int) -> str</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def login_with_context**(login_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `6` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
</span>
</span>

## AuthenticationClientNX
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`AuthenticationClientNX`](#authenticationclientnx).</span>

<code>**async def validate_and_request_ticket**(username: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `1` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def validate_and_request_ticket_with_custom_data**(username: str, extra_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `2` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
<code>source_key: str</code><br>
</span>
</span>

<code>**async def request_ticket**(source: int, target: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `3` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>ticket: bytes</code><br>
<code>key: str</code><br>
</span>
</span>

<code>**async def get_pid**(username: str) -> int</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def get_name**(pid: int) -> str</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def validate_and_request_ticket_with_param**(param: [ValidateAndRequestTicketParam](#validateandrequestticketparam)) -> [ValidateAndRequestTicketResult](#validateandrequestticketresult)</code><br>
<span class="docs">Calls method `6` on the server.</span>

## AuthenticationServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`AuthenticationServer`](#authenticationserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def login**(client: [RMCClient](rmc.md#rmcclient), username: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def login_ex**(client: [RMCClient](rmc.md#rmcclient), username: str, extra_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def request_ticket**(client: [RMCClient](rmc.md#rmcclient), source: int, target: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>ticket: bytes</code><br>
</span>
</span>

<code>**async def get_pid**(client: [RMCClient](rmc.md#rmcclient), username: str) -> int</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def get_name**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> str</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def login_with_context**(client: [RMCClient](rmc.md#rmcclient), login_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
</span>
</span>

## AuthenticationServerNX
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`AuthenticationServerNX`](#authenticationservernx).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def validate_and_request_ticket**(client: [RMCClient](rmc.md#rmcclient), username: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
</span>
</span>

<code>**async def validate_and_request_ticket_with_custom_data**(client: [RMCClient](rmc.md#rmcclient), username: str, extra_data: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>connection_data: [RVConnectionData](#rvconnectiondata)</code><br>
<code>server_name: str</code><br>
<code>source_key: str</code><br>
</span>
</span>

<code>**async def request_ticket**(client: [RMCClient](rmc.md#rmcclient), source: int, target: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](common.md#result)</code><br>
<code>ticket: bytes</code><br>
<code>key: str</code><br>
</span>
</span>

<code>**async def get_pid**(client: [RMCClient](rmc.md#rmcclient), username: str) -> int</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def get_name**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> str</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def validate_and_request_ticket_with_param**(client: [RMCClient](rmc.md#rmcclient), param: [ValidateAndRequestTicketParam](#validateandrequestticketparam)) -> [ValidateAndRequestTicketResult](#validateandrequestticketresult)</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

## AuthenticationInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `AuthenticationInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>token: str</code><br>
<code>ngs_version: int = 3</code><br>
<code>token_type: int = 1</code><br>
<code>server_version: int = 0</code><br>
</span><br>

## RVConnectionData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `RVConnectionData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>main_station: [StationURL](common.md#stationurl) = "prudp:/"</code><br>
<code>special_protocols: list[int] = []</code><br>
<code>special_station: [StationURL](common.md#stationurl) = "prudp:/"</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
If `revision` >= 1:<br>
<span class="docs">
<code>server_time: [DateTime](common.md#datetime) = [DateTime](common.md#datetime).never()</code><br>
</span><br>
</span><br>
</span><br>

## ValidateAndRequestTicketParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ValidateAndRequestTicketParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>platform: int = 3</code><br>
<code>username: str</code><br>
<code>data: [Data](common.md)</code><br>
<code>skip_version_check: bool = False</code><br>
<code>nex_version: int</code><br>
<code>client_version: int</code><br>
</span><br>

## ValidateAndRequestTicketResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ValidateAndRequestTicketResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>ticket: bytes</code><br>
<code>server_url: [StationURL](common.md#stationurl)</code><br>
<code>server_time: [DateTime](common.md#datetime)</code><br>
<code>server_name: str</code><br>
<code>source_key: str</code><br>
</span><br>

