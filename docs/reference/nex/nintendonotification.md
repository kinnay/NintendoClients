
# Module: <code>nintendo.nex.nintendonotification</code>

Provides a client and server for the `NintendoNotificationProtocol`. This page was generated automatically from `nintendonotification.proto`.

<code>**class** [NintendoNotificationClient](#nintendonotificationclient)</code><br>
<span class="docs">The client for the `NintendoNotificationProtocol`.</span>

<code>**class** [NintendoNotificationServer](#nintendonotificationserver)</code><br>
<span class="docs">The server for the `NintendoNotificationProtocol`.</span>

<code>**class** [NintendoNotificationType](#nintendonotificationtype)</code><br>

<code>**class** [NintendoNotificationEvent](#nintendonotificationevent)([Structure](../common))</code><br>
<code>**class** [NintendoNotificationEventGeneral](#nintendonotificationeventgeneral)([Data](../common))</code><br>
<code>**class** [NintendoNotificationEventKeyValue](#nintendonotificationeventkeyvalue)([Data](../common))</code><br>
<code>**class** [NintendoNotificationEventProfile](#nintendonotificationeventprofile)([Data](../common))</code><br>
<code>**class** [StringKeyValue](#stringkeyvalue)([Data](../common))</code><br>
<code>**class** [u32KeyValue](#u32keyvalue)([Data](../common))</code><br>
<code>**class** [u64KeyValue](#u64keyvalue)([Data](../common))</code><br>
<code>**class** [u8KeyValue](#u8keyvalue)([Data](../common))</code><br>

## NintendoNotificationClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`NintendoNotificationClient`](#nintendonotificationclient).</span>

<code>**async def process_nintendo_notification_event**(event: [NintendoNotificationEvent](#nintendonotificationevent)) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def process_nintendo_notification_event_alt**(event: [NintendoNotificationEvent](#nintendonotificationevent)) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

## NintendoNotificationServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`NintendoNotificationServer`](#nintendonotificationserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. Maybe be overridden by a subclass.</span>

<code>**async def process_nintendo_notification_event**(client: [RMCClient](../rmc#rmcclient), event: [NintendoNotificationEvent](#nintendonotificationevent)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def process_nintendo_notification_event_alt**(client: [RMCClient](../rmc#rmcclient), event: [NintendoNotificationEvent](#nintendonotificationevent)) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

## NintendoNotificationType
This class defines the following constants:<br>
<span class="docs">
`LOGOUT = 10`<br>
`PRESENCE_CHANGE = 24`<br>
`UNFRIENDED = 26`<br>
`FRIENDED = 30`<br>
`STATUS_CHANGE = 33`<br>
</span>

## NintendoNotificationEvent
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoNotificationEvent` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>type: int</code><br>
<code>pid: int</code><br>
<code>data: [Data](../common)</code><br>
</span><br>

## NintendoNotificationEventGeneral
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoNotificationEventGeneral` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>param1: int</code><br>
<code>param2: int</code><br>
<code>param3: int</code><br>
<code>text: str</code><br>
</span><br>

## NintendoNotificationEventKeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoNotificationEventKeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>u8: list[[u8KeyValue](#u8keyvalue)]</code><br>
<code>u32: list[[u32KeyValue](#u32keyvalue)]</code><br>
<code>u64: list[[u64KeyValue](#u64keyvalue)]</code><br>
<code>string: list[[StringKeyValue](#stringkeyvalue)]</code><br>
</span><br>

## NintendoNotificationEventProfile
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoNotificationEventProfile` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>region: int</code><br>
<code>country: int</code><br>
<code>area: int</code><br>
<code>language: int</code><br>
<code>platform: int</code><br>
</span><br>

## StringKeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `StringKeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: int</code><br>
<code>value: str</code><br>
</span><br>

## u32KeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `u32KeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: int</code><br>
<code>value: int</code><br>
</span><br>

## u64KeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `u64KeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: int</code><br>
<code>value: int</code><br>
</span><br>

## u8KeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `u8KeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: int</code><br>
<code>value: int</code><br>
</span><br>

