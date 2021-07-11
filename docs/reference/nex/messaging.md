
# Module: <code>nintendo.nex.messaging</code>

Provides a client and server for the `MessagingProtocol` and `MessageDeliveryProtocol`. This page was generated automatically from `messaging.proto`.

<code>**class** [MessagingClient](#messagingclient)</code><br>
<span class="docs">The client for the `MessagingProtocol`.</span>

<code>**class** [MessageDeliveryClient](#messagedeliveryclient)</code><br>
<span class="docs">The client for the `MessageDeliveryProtocol`.</span>

<code>**class** [MessagingServer](#messagingserver)</code><br>
<span class="docs">The server for the `MessagingProtocol`.</span>

<code>**class** [MessageDeliveryServer](#messagedeliveryserver)</code><br>
<span class="docs">The server for the `MessageDeliveryProtocol`.</span>

<code>**class** [RecipientType](#recipienttype)</code><br>

<code>**class** [BinaryMessage](#binarymessage)([UserMessage](#usermessage))</code><br>
<code>**class** [MessageRecipient](#messagerecipient)([Structure](common.md))</code><br>
<code>**class** [TextMessage](#textmessage)([UserMessage](#usermessage))</code><br>
<code>**class** [UserMessage](#usermessage)([Data](common.md))</code><br>

## MessagingClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MessagingClient`](#messagingclient).</span>

<code>**async def deliver_message**(message: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `1` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>modified_message: [Data](common.md)</code><br>
<code>sandbox_node_ids: list[int]</code><br>
<code>participants: list[int]</code><br>
</span>
</span>

<code>**async def get_number_of_messages**(recipient: [MessageRecipient](#messagerecipient)) -> int</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def get_message_headers**(recipient: [MessageRecipient](#messagerecipient), range: [ResultRange](common.md#resultrange)) -> list[[UserMessage](#usermessage)]</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def retrieve_all_messages_within_range**(recipient: [MessageRecipient](#messagerecipient), range: [ResultRange](common.md#resultrange)) -> list[[Data](common.md)]</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def retrieve_messages**(recipient: [MessageRecipient](#messagerecipient), message_ids: list[int], leave_on_server: bool) -> list[[Data](common.md)]</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def delete_messages**(recipient: [MessageRecipient](#messagerecipient), message_ids: list[int]) -> None</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def delete_all_messages**(recipient: [MessageRecipient](#messagerecipient)) -> int</code><br>
<span class="docs">Calls method `7` on the server.</span>

## MessageDeliveryClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`MessageDeliveryClient`](#messagedeliveryclient).</span>

<code>**async def deliver_message**(message: [Data](common.md)) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

## MessagingServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MessagingServer`](#messagingserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def deliver_message**(client: [RMCClient](rmc.md#rmcclient), message: [Data](common.md)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>modified_message: [Data](common.md)</code><br>
<code>sandbox_node_ids: list[int]</code><br>
<code>participants: list[int]</code><br>
</span>
</span>

<code>**async def get_number_of_messages**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient)) -> int</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def get_message_headers**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient), range: [ResultRange](common.md#resultrange)) -> list[[UserMessage](#usermessage)]</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def retrieve_all_messages_within_range**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient), range: [ResultRange](common.md#resultrange)) -> list[[Data](common.md)]</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def retrieve_messages**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient), message_ids: list[int], leave_on_server: bool) -> list[[Data](common.md)]</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def delete_messages**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient), message_ids: list[int]) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def delete_all_messages**(client: [RMCClient](rmc.md#rmcclient), recipient: [MessageRecipient](#messagerecipient)) -> int</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

## MessageDeliveryServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`MessageDeliveryServer`](#messagedeliveryserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def deliver_message**(client: [RMCClient](rmc.md#rmcclient), message: [Data](common.md)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

## RecipientType
This class defines the following constants:<br>
<span class="docs">
`PRINCIPAL = 1`<br>
`GATHERING = 2`<br>
</span>

## BinaryMessage
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BinaryMessage` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>body: bytes</code><br>
</span><br>

## MessageRecipient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MessageRecipient` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>type: int</code><br>
<code>pid: int</code><br>
<code>gid: int</code><br>
</span><br>

## TextMessage
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `TextMessage` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>body: str</code><br>
</span><br>

## UserMessage
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `UserMessage` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>id: int</code><br>
<code>parent_id: int</code><br>
<code>sender: int</code><br>
<code>reception_time: [DateTime](common.md#datetime)</code><br>
<code>life_time: int</code><br>
<code>flags: int</code><br>
<code>subject: str</code><br>
<code>sender_name: str</code><br>
<code>recipient: [MessageRecipient](#messagerecipient) = [MessageRecipient](#messagerecipient)()</code><br>
</span><br>

