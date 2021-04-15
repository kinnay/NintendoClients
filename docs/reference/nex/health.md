
# Module: <code>nintendo.nex.health</code>

Provides a client and server for the `HealthProtocol`. This page was generated automatically from `health.proto`.

<code>**class** [HealthClient](#healthclient)</code><br>
<span class="docs">The client for the `HealthProtocol`.</span>

<code>**class** [HealthServer](#healthserver)</code><br>
<span class="docs">The server for the `HealthProtocol`.</span>

## HealthClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`HealthClient`](#healthclient).</span>

<code>**async def ping_daemon**() -> bool</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def ping_database**() -> bool</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def run_sanity_check**() -> bool</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def fix_sanity_errors**() -> bool</code><br>
<span class="docs">Calls method `4` on the server.</span>

## HealthServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`HealthServer`](#healthserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def ping_daemon**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def ping_database**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def run_sanity_check**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def fix_sanity_errors**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

