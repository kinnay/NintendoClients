
# Module: <code>nintendo.nex.notification</code>

Provides a client and server for the `NotificationProtocol`. This page was generated automatically from `notification.proto`.

<code>**class** [NotificationClient](#notificationclient)</code><br>
<span class="docs">The client for the `NotificationProtocol`.</span>

<code>**class** [NotificationServer](#notificationserver)</code><br>
<span class="docs">The server for the `NotificationProtocol`.</span>

<code>**class** [NotificationEvent](#notificationevent)([Structure](../common))</code><br>

## NotificationClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`NotificationClient`](#notificationclient).</span>

<code>**async def process_notification_event**(event: [NotificationEvent](../notification#notificationevent)) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

## NotificationServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`NotificationServer`](#notificationserver).</span>

<code>**async def logout**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def process_notification_event**(client: [RMCClient](../rmc#rmcclient), event: [NotificationEvent](../notification#notificationevent)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

## NotificationEvent
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NotificationEvent` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>type: int</code><br>
<code>param1: int = 0</code><br>
<code>param2: int = 0</code><br>
<code>text: str = ""</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>param3: int = 0</code><br>
</span><br>
If `nex.version` >= 40000:<br>
<span class="docs">
<code>map: dict[str, object] = {}</code><br>
</span><br>
</span><br>

