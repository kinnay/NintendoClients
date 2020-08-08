
# Module: <code>nintendo.nex.friends</code>

Provides a client and server for the `FriendsProtocolV1` and `FriendsProtocolV2`. This page was generated automatically from `friends.proto`.

<code>**class** [FriendsClientV1](#friendsclientv1)</code><br>
<span class="docs">The client for the `FriendsProtocolV1`.</span>

<code>**class** [FriendsClientV2](#friendsclientv2)</code><br>
<span class="docs">The client for the `FriendsProtocolV2`.</span>

<code>**class** [FriendsServerV1](#friendsserverv1)</code><br>
<span class="docs">The server for the `FriendsProtocolV1`.</span>

<code>**class** [FriendsServerV2](#friendsserverv2)</code><br>
<span class="docs">The server for the `FriendsProtocolV2`.</span>

<code>**class** [BlacklistedPrincipal](#blacklistedprincipal)([Data](../common))</code><br>
<code>**class** [Comment](#comment)([Data](../common))</code><br>
<code>**class** [FriendInfo](#friendinfo)([Data](../common))</code><br>
<code>**class** [FriendRequest](#friendrequest)([Data](../common))</code><br>
<code>**class** [FriendRequestMessage](#friendrequestmessage)([Data](../common))</code><br>
<code>**class** [GameKey](#gamekey)([Data](../common))</code><br>
<code>**class** [MiiV2](#miiv2)([Data](../common))</code><br>
<code>**class** [NNAInfo](#nnainfo)([Data](../common))</code><br>
<code>**class** [NintendoCreateAccountData](#nintendocreateaccountdata)([Data](../common))</code><br>
<code>**class** [NintendoPresenceV2](#nintendopresencev2)([Data](../common))</code><br>
<code>**class** [PersistentNotification](#persistentnotification)([Data](../common))</code><br>
<code>**class** [PrincipalBasicInfo](#principalbasicinfo)([Data](../common))</code><br>
<code>**class** [PrincipalPreference](#principalpreference)([Data](../common))</code><br>
<code>**class** [PrincipalRequestBlockSetting](#principalrequestblocksetting)([Structure](../common))</code><br>

## FriendsClientV1
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`FriendsClientV1`](#friendsclientv1).</span>

## FriendsClientV2
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`FriendsClientV2`](#friendsclientv2).</span>

<code>**async def update_and_get_all_information**(nna_info: [NNAInfo](#nnainfo), presence: [NintendoPresenceV2](#nintendopresencev2), birthday: [DateTime](../common#datetime)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `1` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>principal_preference: [PrincipalPreference](#principalpreference)</code><br>
<code>comment: [Comment](#comment)</code><br>
<code>friends: list[[FriendInfo](#friendinfo)]</code><br>
<code>sent_requests: list[[FriendRequest](#friendrequest)]</code><br>
<code>received_requests: list[[FriendRequest](#friendrequest)]</code><br>
<code>blacklist: list[[BlacklistedPrincipal](#blacklistedprincipal)]</code><br>
<code>unk1: bool</code><br>
<code>notifications: list[[PersistentNotification](#persistentnotification)]</code><br>
<code>unk2: bool</code><br>
</span>
</span>

<code>**async def add_friend**(pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `2` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def add_friend_by_name**(name: str) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `3` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def remove_friend**(pid: int) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def add_friend_request**(unk1: int, unk2: int, unk3: str, unk4: int, unk5: str, game_key: [GameKey](#gamekey), unk6: [DateTime](../common#datetime)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `5` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def cancel_friend_request**(id: int) -> None</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def accept_friend_request**(id: int) -> [FriendInfo](#friendinfo)</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def delete_friend_request**(id: int) -> None</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def deny_friend_request**(id: int) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def mark_friend_requests_as_received**(ids: list[int]) -> None</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def add_black_list**(principal: [BlacklistedPrincipal](#blacklistedprincipal)) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def remove_black_list**(pid: int) -> None</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def update_presence**(presence: [NintendoPresenceV2](#nintendopresencev2)) -> None</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def update_mii**(mii: [MiiV2](#miiv2)) -> [DateTime](../common#datetime)</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def update_comment**(comment: [Comment](#comment)) -> [DateTime](../common#datetime)</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def update_preference**(preference: [PrincipalPreference](#principalpreference)) -> None</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def get_basic_info**(pids: list[int]) -> list[[PrincipalBasicInfo](#principalbasicinfo)]</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def delete_persistent_notification**(notifications: list[[PersistentNotification](#persistentnotification)]) -> None</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def check_setting_status**() -> int</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def get_request_block_settings**(unk: list[int]) -> list[[PrincipalRequestBlockSetting](#principalrequestblocksetting)]</code><br>
<span class="docs">Calls method `20` on the server.</span>

## FriendsServerV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`FriendsServerV1`](#friendsserverv1).</span>

## FriendsServerV2
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`FriendsServerV2`](#friendsserverv2).</span>

<code>**async def update_and_get_all_information**(client: [RMCClient](../rmc#rmcclient), nna_info: [NNAInfo](#nnainfo), presence: [NintendoPresenceV2](#nintendopresencev2), birthday: [DateTime](../common#datetime)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>principal_preference: [PrincipalPreference](#principalpreference)</code><br>
<code>comment: [Comment](#comment)</code><br>
<code>friends: list[[FriendInfo](#friendinfo)]</code><br>
<code>sent_requests: list[[FriendRequest](#friendrequest)]</code><br>
<code>received_requests: list[[FriendRequest](#friendrequest)]</code><br>
<code>blacklist: list[[BlacklistedPrincipal](#blacklistedprincipal)]</code><br>
<code>unk1: bool</code><br>
<code>notifications: list[[PersistentNotification](#persistentnotification)]</code><br>
<code>unk2: bool</code><br>
</span>
</span>

<code>**async def add_friend**(client: [RMCClient](../rmc#rmcclient), pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def add_friend_by_name**(client: [RMCClient](../rmc#rmcclient), name: str) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def remove_friend**(client: [RMCClient](../rmc#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def add_friend_request**(client: [RMCClient](../rmc#rmcclient), unk1: int, unk2: int, unk3: str, unk4: int, unk5: str, game_key: [GameKey](#gamekey), unk6: [DateTime](../common#datetime)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def cancel_friend_request**(client: [RMCClient](../rmc#rmcclient), id: int) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def accept_friend_request**(client: [RMCClient](../rmc#rmcclient), id: int) -> [FriendInfo](#friendinfo)</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def delete_friend_request**(client: [RMCClient](../rmc#rmcclient), id: int) -> None</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def deny_friend_request**(client: [RMCClient](../rmc#rmcclient), id: int) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def mark_friend_requests_as_received**(client: [RMCClient](../rmc#rmcclient), ids: list[int]) -> None</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def add_black_list**(client: [RMCClient](../rmc#rmcclient), principal: [BlacklistedPrincipal](#blacklistedprincipal)) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def remove_black_list**(client: [RMCClient](../rmc#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def update_presence**(client: [RMCClient](../rmc#rmcclient), presence: [NintendoPresenceV2](#nintendopresencev2)) -> None</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def update_mii**(client: [RMCClient](../rmc#rmcclient), mii: [MiiV2](#miiv2)) -> [DateTime](../common#datetime)</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def update_comment**(client: [RMCClient](../rmc#rmcclient), comment: [Comment](#comment)) -> [DateTime](../common#datetime)</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def update_preference**(client: [RMCClient](../rmc#rmcclient), preference: [PrincipalPreference](#principalpreference)) -> None</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def get_basic_info**(client: [RMCClient](../rmc#rmcclient), pids: list[int]) -> list[[PrincipalBasicInfo](#principalbasicinfo)]</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def delete_persistent_notification**(client: [RMCClient](../rmc#rmcclient), notifications: list[[PersistentNotification](#persistentnotification)]) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def check_setting_status**(client: [RMCClient](../rmc#rmcclient)) -> int</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def get_request_block_settings**(client: [RMCClient](../rmc#rmcclient), unk: list[int]) -> list[[PrincipalRequestBlockSetting](#principalrequestblocksetting)]</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

## BlacklistedPrincipal
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BlacklistedPrincipal` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>principal_info: [PrincipalBasicInfo](#principalbasicinfo) = [PrincipalBasicInfo](#principalbasicinfo)()</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>since: [DateTime](../common#datetime)</code><br>
</span><br>

## Comment
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Comment` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk: int</code><br>
<code>text: str</code><br>
<code>changed: [DateTime](../common#datetime)</code><br>
</span><br>

## FriendInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>nna_info: [NNAInfo](#nnainfo) = [NNAInfo](#nnainfo)()</code><br>
<code>presence: [NintendoPresenceV2](#nintendopresencev2) = [NintendoPresenceV2](#nintendopresencev2)()</code><br>
<code>comment: [Comment](#comment) = [Comment](#comment)()</code><br>
<code>befriended: [DateTime](../common#datetime)</code><br>
<code>last_online: [DateTime](../common#datetime)</code><br>
<code>unk: int</code><br>
</span><br>

## FriendRequest
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendRequest` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>principal_info: [PrincipalBasicInfo](#principalbasicinfo) = [PrincipalBasicInfo](#principalbasicinfo)()</code><br>
<code>message: [FriendRequestMessage](#friendrequestmessage) = [FriendRequestMessage](#friendrequestmessage)()</code><br>
<code>sent: [DateTime](../common#datetime)</code><br>
</span><br>

## FriendRequestMessage
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendRequestMessage` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: int</code><br>
<code>unk3: int</code><br>
<code>message: str</code><br>
<code>unk4: int</code><br>
<code>string: str</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>datetime: [DateTime](../common#datetime)</code><br>
<code>expires: [DateTime](../common#datetime)</code><br>
</span><br>

## GameKey
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `GameKey` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>title_id: int = 0</code><br>
<code>title_version: int = 0</code><br>
</span><br>

## MiiV2
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MiiV2` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>name: str</code><br>
<code>unk1: int = 0</code><br>
<code>unk2: int = 0</code><br>
<code>data: bytes</code><br>
<code>datetime: [DateTime](../common#datetime) = [DateTime](../common#datetime).never()</code><br>
</span><br>

## NNAInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NNAInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>principal_info: [PrincipalBasicInfo](#principalbasicinfo) = [PrincipalBasicInfo](#principalbasicinfo)()</code><br>
<code>unk1: int = 94</code><br>
<code>unk2: int = 11</code><br>
</span><br>

## NintendoCreateAccountData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoCreateAccountData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>info: [NNAInfo](#nnainfo) = [NNAInfo](#nnainfo)()</code><br>
<code>token: str</code><br>
<code>birthday: [DateTime](../common#datetime)</code><br>
<code>unk: int</code><br>
</span><br>

## NintendoPresenceV2
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoPresenceV2` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>flags: int = 0</code><br>
<code>is_online: bool = False</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>unk1: int = 0</code><br>
<code>message: str = ""</code><br>
<code>unk2: int = 0</code><br>
<code>unk3: int = 0</code><br>
<code>game_server_id: int = 0</code><br>
<code>unk4: int = 0</code><br>
<code>pid: int = 0</code><br>
<code>gathering_id: int = 0</code><br>
<code>application_data: bytes = b""</code><br>
<code>unk5: int = 3</code><br>
<code>unk6: int = 3</code><br>
<code>unk7: int = 3</code><br>
</span><br>

## PersistentNotification
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PersistentNotification` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: int</code><br>
<code>unk3: int</code><br>
<code>unk4: int</code><br>
<code>string: str</code><br>
</span><br>

## PrincipalBasicInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PrincipalBasicInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>nnid: str</code><br>
<code>mii: [MiiV2](#miiv2) = [MiiV2](#miiv2)()</code><br>
<code>unk: int = 2</code><br>
</span><br>

## PrincipalPreference
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PrincipalPreference` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: bool</code><br>
<code>unk2: bool</code><br>
<code>unk3: bool</code><br>
</span><br>

## PrincipalRequestBlockSetting
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PrincipalRequestBlockSetting` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: bool</code><br>
</span><br>

