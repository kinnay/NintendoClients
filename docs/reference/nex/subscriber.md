
# Module: <code>nintendo.nex.subscriber</code>

Provides a client and server for the `SubscriberProtocol`. This page was generated automatically from `subscriber.proto`.

<code>**class** [SubscriberClient](#subscriberclient)</code><br>
<span class="docs">The client for the `SubscriberProtocol`.</span>

<code>**class** [SubscriberServer](#subscriberserver)</code><br>
<span class="docs">The server for the `SubscriberProtocol`.</span>

## SubscriberClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`SubscriberClient`](#subscriberclient).</span>

## SubscriberServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`SubscriberServer`](#subscriberserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

