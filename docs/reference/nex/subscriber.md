
# Module: <code>nintendo.nex.subscriber</code>

Provides a client and server for the `SubscriberProtocol`. This page was generated automatically from `subscriber.proto`.

<code>**class** [SubscriberClient](#subscriberclient)</code><br>
<span class="docs">The client for the `SubscriberProtocol`.</span>

<code>**class** [SubscriberServer](#subscriberserver)</code><br>
<span class="docs">The server for the `SubscriberProtocol`.</span>

## SubscriberClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`SubscriberClient`](#subscriberclient).</span>

## SubscriberServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`SubscriberServer`](#subscriberserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

