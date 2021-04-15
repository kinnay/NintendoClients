
# Module: <code>nintendo.nex.aauser</code>

Provides a client and server for the `AAUserProtocol`. This page was generated automatically from `aauser.proto`.

<code>**class** [AAUserClient](#aauserclient)</code><br>
<span class="docs">The client for the `AAUserProtocol`.</span>

<code>**class** [AAUserServer](#aauserserver)</code><br>
<span class="docs">The server for the `AAUserProtocol`.</span>

<code>**class** [ApplicationInfo](#applicationinfo)([Structure](../common))</code><br>

## AAUserClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`AAUserClient`](#aauserclient).</span>

<code>**async def register_application**(title_id: int) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def unregister_application**(title_id: int) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def set_application_info**(application_info: list[[ApplicationInfo](#applicationinfo)]) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def get_application_info**() -> list[[ApplicationInfo](#applicationinfo)]</code><br>
<span class="docs">Calls method `4` on the server.</span>

## AAUserServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`AAUserServer`](#aauserserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def register_application**(client: [RMCClient](../rmc#rmcclient), title_id: int) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def unregister_application**(client: [RMCClient](../rmc#rmcclient), title_id: int) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def set_application_info**(client: [RMCClient](../rmc#rmcclient), application_info: list[[ApplicationInfo](#applicationinfo)]) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def get_application_info**(client: [RMCClient](../rmc#rmcclient)) -> list[[ApplicationInfo](#applicationinfo)]</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

## ApplicationInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ApplicationInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>title_id: int</code><br>
<code>title_version: int</code><br>
</span><br>

