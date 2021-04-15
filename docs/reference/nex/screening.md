
# Module: <code>nintendo.nex.screening</code>

Provides a client and server for the `ScreeningProtocol`. This page was generated automatically from `screening.proto`.

<code>**class** [ScreeningClient](#screeningclient)</code><br>
<span class="docs">The client for the `ScreeningProtocol`.</span>

<code>**class** [ScreeningServer](#screeningserver)</code><br>
<span class="docs">The server for the `ScreeningProtocol`.</span>

## ScreeningClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`ScreeningClient`](#screeningclient).</span>

## ScreeningServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`ScreeningServer`](#screeningserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

