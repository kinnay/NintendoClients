
# Module: <code>nintendo.nex.screening</code>

Provides a client and server for the `ScreeningProtocol`. This page was generated automatically from `screening.proto`.

<code>**class** [ScreeningClient](#screeningclient)</code><br>
<span class="docs">The client for the `ScreeningProtocol`.</span>

<code>**class** [ScreeningServer](#screeningserver)</code><br>
<span class="docs">The server for the `ScreeningProtocol`.</span>

## ScreeningClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`ScreeningClient`](#screeningclient).</span>

## ScreeningServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`ScreeningServer`](#screeningserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

