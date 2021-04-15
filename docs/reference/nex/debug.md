
# Module: <code>nintendo.nex.debug</code>

Provides a client and server for the `DebugProtocol`. This page was generated automatically from `debug.proto`.

<code>**class** [DebugClient](#debugclient)</code><br>
<span class="docs">The client for the `DebugProtocol`.</span>

<code>**class** [DebugServer](#debugserver)</code><br>
<span class="docs">The server for the `DebugProtocol`.</span>

<code>**class** [ApiCall](#apicall)([Structure](../common))</code><br>

## DebugClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`DebugClient`](#debugclient).</span>

<code>**async def enable_api_recorder**() -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def disable_api_recorder**() -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def is_api_recorder_enabled**() -> bool</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def get_api_calls**(pids: list[int], unk1: [DateTime](../common#datetime), unk2: [DateTime](../common#datetime)) -> list[[ApiCall](#apicall)]</code><br>
<span class="docs">Calls method `4` on the server.</span>

## DebugServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`DebugServer`](#debugserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def enable_api_recorder**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def disable_api_recorder**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def is_api_recorder_enabled**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def get_api_calls**(client: [RMCClient](../rmc#rmcclient), pids: list[int], unk1: [DateTime](../common#datetime), unk2: [DateTime](../common#datetime)) -> list[[ApiCall](#apicall)]</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

## ApiCall
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ApiCall` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>name: str</code><br>
<code>time: [DateTime](../common#datetime)</code><br>
<code>pid: int</code><br>
</span><br>

