
# Module: <code>nintendo.nex.remotelog</code>

Provides a client and server for the `RemoteLogDeviceProtocol`. This page was generated automatically from `remotelog.proto`.

<code>**class** [RemoteLogDeviceClient](#remotelogdeviceclient)</code><br>
<span class="docs">The client for the `RemoteLogDeviceProtocol`.</span>

<code>**class** [RemoteLogDeviceServer](#remotelogdeviceserver)</code><br>
<span class="docs">The server for the `RemoteLogDeviceProtocol`.</span>

## RemoteLogDeviceClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`RemoteLogDeviceClient`](#remotelogdeviceclient).</span>

<code>**async def log**(message: str) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

## RemoteLogDeviceServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`RemoteLogDeviceServer`](#remotelogdeviceserver).</span>

<code>**async def logout**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def log**(client: [RMCClient](../rmc#rmcclient), message: str) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

