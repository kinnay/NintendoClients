
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

<code>**class** [AccountExtraInfo](#accountextrainfo)([Structure](common.md))</code><br>
<code>**class** [BlacklistedPrincipal](#blacklistedprincipal)([Data](common.md))</code><br>
<code>**class** [Comment](#comment)([Data](common.md))</code><br>
<code>**class** [FriendComment](#friendcomment)([Data](common.md))</code><br>
<code>**class** [FriendInfo](#friendinfo)([Data](common.md))</code><br>
<code>**class** [FriendKey](#friendkey)([Structure](common.md))</code><br>
<code>**class** [FriendMii](#friendmii)([Data](common.md))</code><br>
<code>**class** [FriendMiiList](#friendmiilist)([Data](common.md))</code><br>
<code>**class** [FriendPersistentInfo](#friendpersistentinfo)([Data](common.md))</code><br>
<code>**class** [FriendPicture](#friendpicture)([Data](common.md))</code><br>
<code>**class** [FriendPresence](#friendpresence)([Data](common.md))</code><br>
<code>**class** [FriendRelationship](#friendrelationship)([Data](common.md))</code><br>
<code>**class** [FriendRequest](#friendrequest)([Data](common.md))</code><br>
<code>**class** [FriendRequestMessage](#friendrequestmessage)([Data](common.md))</code><br>
<code>**class** [GameKey](#gamekey)([Data](common.md))</code><br>
<code>**class** [Mii](#mii)([Data](common.md))</code><br>
<code>**class** [MiiList](#miilist)([Data](common.md))</code><br>
<code>**class** [MiiV2](#miiv2)([Data](common.md))</code><br>
<code>**class** [MyProfile](#myprofile)([Data](common.md))</code><br>
<code>**class** [NNAInfo](#nnainfo)([Data](common.md))</code><br>
<code>**class** [NintendoCreateAccountData](#nintendocreateaccountdata)([Data](common.md))</code><br>
<code>**class** [NintendoPresence](#nintendopresence)([Data](common.md))</code><br>
<code>**class** [NintendoPresenceV2](#nintendopresencev2)([Data](common.md))</code><br>
<code>**class** [PersistentNotification](#persistentnotification)([Data](common.md))</code><br>
<code>**class** [PlayedGame](#playedgame)([Data](common.md))</code><br>
<code>**class** [PrincipalBasicInfo](#principalbasicinfo)([Data](common.md))</code><br>
<code>**class** [PrincipalPreference](#principalpreference)([Data](common.md))</code><br>
<code>**class** [PrincipalRequestBlockSetting](#principalrequestblocksetting)([Data](common.md))</code><br>

## FriendsClientV1
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`FriendsClientV1`](#friendsclientv1).</span>

<code>**async def update_profile**(profile_data: [MyProfile](#myprofile)) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def update_mii**(mii: [Mii](#mii)) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def update_mii_list**(mii_list: [MiiList](#miilist)) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def update_played_games**(played_games: list[[PlayedGame](#playedgame)]) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def update_preference**(unk1: bool, unk2: bool, unk3: bool) -> None</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_friend_mii**(friends: list[[FriendKey](#friendkey)]) -> list[[FriendMii](#friendmii)]</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def get_friend_mii_list**(friends: list[[FriendKey](#friendkey)]) -> list[[FriendMiiList](#friendmiilist)]</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def is_active_game**(unk1: list[int], game_key: [GameKey](#gamekey)) -> list[int]</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_principal_id_by_local_friend_code**(unk1: int, unk2: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `9` on the server.</span>

<code>**async def get_friend_relationships**(unk: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def add_friend_by_principal_id**(unk: int, pid: int) -> [FriendRelationship](#friendrelationship)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def add_friend_by_principal_ids**(unk: int, pids: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def remove_friend_by_local_friend_code**(friend_code: int) -> None</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def remove_friend_by_principal_id**(pid: int) -> None</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def get_all_friends**() -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def update_black_list**(unk: list[int]) -> None</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def sync_friend**(unk1: int, unk2: list[int], unk3: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def update_presence**(presence_info: [NintendoPresence](#nintendopresence), unk: bool) -> None</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def update_favorite_game_key**(game_key: [GameKey](#gamekey)) -> None</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def update_comment**(comment: str) -> None</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def update_picture**(unk: int, picture: bytes) -> None</code><br>
<span class="docs">Calls method `21` on the server.</span>

<code>**async def get_friend_presence**(unk: list[int]) -> list[[FriendPresence](#friendpresence)]</code><br>
<span class="docs">Calls method `22` on the server.</span>

<code>**async def get_friend_comment**(friends: list[[FriendKey](#friendkey)]) -> list[[FriendComment](#friendcomment)]</code><br>
<span class="docs">Calls method `23` on the server.</span>

<code>**async def get_friend_picture**(unk: list[int]) -> list[[FriendPicture](#friendpicture)]</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def get_friend_persistent_info**(unk: list[int]) -> list[[FriendPersistentInfo](#friendpersistentinfo)]</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def send_invitation**(unk: list[int]) -> None</code><br>
<span class="docs">Calls method `26` on the server.</span>

## FriendsClientV2
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`FriendsClientV2`](#friendsclientv2).</span>

<code>**async def update_and_get_all_information**(nna_info: [NNAInfo](#nnainfo), presence: [NintendoPresenceV2](#nintendopresencev2), birthday: [DateTime](common.md#datetime)) -> [RMCResponse](common.md)</code><br>
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

<code>**async def add_friend**(pid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `2` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def add_friend_by_name**(name: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Calls method `3` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def remove_friend**(pid: int) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def add_friend_request**(unk1: int, unk2: int, unk3: str, unk4: int, unk5: str, game_key: [GameKey](#gamekey), unk6: [DateTime](common.md#datetime)) -> [RMCResponse](common.md)</code><br>
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

<code>**async def update_mii**(mii: [MiiV2](#miiv2)) -> [DateTime](common.md#datetime)</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def update_comment**(comment: [Comment](#comment)) -> [DateTime](common.md#datetime)</code><br>
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

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def update_profile**(client: [RMCClient](rmc.md#rmcclient), profile_data: [MyProfile](#myprofile)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def update_mii**(client: [RMCClient](rmc.md#rmcclient), mii: [Mii](#mii)) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def update_mii_list**(client: [RMCClient](rmc.md#rmcclient), mii_list: [MiiList](#miilist)) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def update_played_games**(client: [RMCClient](rmc.md#rmcclient), played_games: list[[PlayedGame](#playedgame)]) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def update_preference**(client: [RMCClient](rmc.md#rmcclient), unk1: bool, unk2: bool, unk3: bool) -> None</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_mii**(client: [RMCClient](rmc.md#rmcclient), friends: list[[FriendKey](#friendkey)]) -> list[[FriendMii](#friendmii)]</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_mii_list**(client: [RMCClient](rmc.md#rmcclient), friends: list[[FriendKey](#friendkey)]) -> list[[FriendMiiList](#friendmiilist)]</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def is_active_game**(client: [RMCClient](rmc.md#rmcclient), unk1: list[int], game_key: [GameKey](#gamekey)) -> list[int]</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_principal_id_by_local_friend_code**(client: [RMCClient](rmc.md#rmcclient), unk1: int, unk2: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_relationships**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def add_friend_by_principal_id**(client: [RMCClient](rmc.md#rmcclient), unk: int, pid: int) -> [FriendRelationship](#friendrelationship)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def add_friend_by_principal_ids**(client: [RMCClient](rmc.md#rmcclient), unk: int, pids: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def remove_friend_by_local_friend_code**(client: [RMCClient](rmc.md#rmcclient), friend_code: int) -> None</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def remove_friend_by_principal_id**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def get_all_friends**(client: [RMCClient](rmc.md#rmcclient)) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def update_black_list**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> None</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def sync_friend**(client: [RMCClient](rmc.md#rmcclient), unk1: int, unk2: list[int], unk3: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def update_presence**(client: [RMCClient](rmc.md#rmcclient), presence_info: [NintendoPresence](#nintendopresence), unk: bool) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def update_favorite_game_key**(client: [RMCClient](rmc.md#rmcclient), game_key: [GameKey](#gamekey)) -> None</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def update_comment**(client: [RMCClient](rmc.md#rmcclient), comment: str) -> None</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def update_picture**(client: [RMCClient](rmc.md#rmcclient), unk: int, picture: bytes) -> None</code><br>
<span class="docs">Handler for method `21`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_presence**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPresence](#friendpresence)]</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_comment**(client: [RMCClient](rmc.md#rmcclient), friends: list[[FriendKey](#friendkey)]) -> list[[FriendComment](#friendcomment)]</code><br>
<span class="docs">Handler for method `23`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_picture**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPicture](#friendpicture)]</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_persistent_info**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPersistentInfo](#friendpersistentinfo)]</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def send_invitation**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> None</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

## FriendsServerV2
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`FriendsServerV2`](#friendsserverv2).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def update_and_get_all_information**(client: [RMCClient](rmc.md#rmcclient), nna_info: [NNAInfo](#nnainfo), presence: [NintendoPresenceV2](#nintendopresencev2), birthday: [DateTime](common.md#datetime)) -> [RMCResponse](common.md)</code><br>
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

<code>**async def add_friend**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def add_friend_by_name**(client: [RMCClient](rmc.md#rmcclient), name: str) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def remove_friend**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def add_friend_request**(client: [RMCClient](rmc.md#rmcclient), unk1: int, unk2: int, unk3: str, unk4: int, unk5: str, game_key: [GameKey](#gamekey), unk6: [DateTime](common.md#datetime)) -> [RMCResponse](common.md)</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>request: [FriendRequest](#friendrequest)</code><br>
<code>info: [FriendInfo](#friendinfo)</code><br>
</span>
</span>

<code>**async def cancel_friend_request**(client: [RMCClient](rmc.md#rmcclient), id: int) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def accept_friend_request**(client: [RMCClient](rmc.md#rmcclient), id: int) -> [FriendInfo](#friendinfo)</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def delete_friend_request**(client: [RMCClient](rmc.md#rmcclient), id: int) -> None</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def deny_friend_request**(client: [RMCClient](rmc.md#rmcclient), id: int) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass.</span>

<code>**async def mark_friend_requests_as_received**(client: [RMCClient](rmc.md#rmcclient), ids: list[int]) -> None</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def add_black_list**(client: [RMCClient](rmc.md#rmcclient), principal: [BlacklistedPrincipal](#blacklistedprincipal)) -> [BlacklistedPrincipal](#blacklistedprincipal)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def remove_black_list**(client: [RMCClient](rmc.md#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def update_presence**(client: [RMCClient](rmc.md#rmcclient), presence: [NintendoPresenceV2](#nintendopresencev2)) -> None</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def update_mii**(client: [RMCClient](rmc.md#rmcclient), mii: [MiiV2](#miiv2)) -> [DateTime](common.md#datetime)</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def update_comment**(client: [RMCClient](rmc.md#rmcclient), comment: [Comment](#comment)) -> [DateTime](common.md#datetime)</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def update_preference**(client: [RMCClient](rmc.md#rmcclient), preference: [PrincipalPreference](#principalpreference)) -> None</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def get_basic_info**(client: [RMCClient](rmc.md#rmcclient), pids: list[int]) -> list[[PrincipalBasicInfo](#principalbasicinfo)]</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def delete_persistent_notification**(client: [RMCClient](rmc.md#rmcclient), notifications: list[[PersistentNotification](#persistentnotification)]) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def check_setting_status**(client: [RMCClient](rmc.md#rmcclient)) -> int</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def get_request_block_settings**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[PrincipalRequestBlockSetting](#principalrequestblocksetting)]</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

## AccountExtraInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `AccountExtraInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: int</code><br>
<code>token: str</code><br>
</span><br>

## BlacklistedPrincipal
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BlacklistedPrincipal` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>principal_info: [PrincipalBasicInfo](#principalbasicinfo) = [PrincipalBasicInfo](#principalbasicinfo)()</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>since: [DateTime](common.md#datetime)</code><br>
</span><br>

## Comment
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Comment` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk: int</code><br>
<code>text: str</code><br>
<code>changed: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendComment
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendComment` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>comment: str</code><br>
<code>unk2: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>nna_info: [NNAInfo](#nnainfo) = [NNAInfo](#nnainfo)()</code><br>
<code>presence: [NintendoPresenceV2](#nintendopresencev2) = [NintendoPresenceV2](#nintendopresencev2)()</code><br>
<code>comment: [Comment](#comment) = [Comment](#comment)()</code><br>
<code>befriended: [DateTime](common.md#datetime)</code><br>
<code>last_online: [DateTime](common.md#datetime)</code><br>
<code>unk: int</code><br>
</span><br>

## FriendKey
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendKey` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendMii
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendMii` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>mii: [Mii](#mii) = [Mii](#mii)()</code><br>
<code>unk2: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendMiiList
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendMiiList` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>mii: [MiiList](#miilist) = [MiiList](#miilist)()</code><br>
<code>unk2: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendPersistentInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendPersistentInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>region: int</code><br>
<code>country: int</code><br>
<code>area: int</code><br>
<code>language: int</code><br>
<code>platform: int</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>message: str</code><br>
<code>message_updated: [DateTime](common.md#datetime)</code><br>
<code>friended: [DateTime](common.md#datetime)</code><br>
<code>unk: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendPicture
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendPicture` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk: int</code><br>
<code>data: bytes</code><br>
<code>datetime: [DateTime](common.md#datetime)</code><br>
</span><br>

## FriendPresence
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendPresence` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk: int</code><br>
<code>presence: [NintendoPresence](#nintendopresence) = [NintendoPresence](#nintendopresence)()</code><br>
</span><br>

## FriendRelationship
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendRelationship` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: int</code><br>
<code>unk3: int</code><br>
</span><br>

## FriendRequest
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendRequest` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>principal_info: [PrincipalBasicInfo](#principalbasicinfo) = [PrincipalBasicInfo](#principalbasicinfo)()</code><br>
<code>message: [FriendRequestMessage](#friendrequestmessage) = [FriendRequestMessage](#friendrequestmessage)()</code><br>
<code>sent: [DateTime](common.md#datetime)</code><br>
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
<code>datetime: [DateTime](common.md#datetime)</code><br>
<code>expires: [DateTime](common.md#datetime)</code><br>
</span><br>

## GameKey
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `GameKey` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>title_id: int = 0</code><br>
<code>title_version: int = 0</code><br>
</span><br>

## Mii
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `Mii` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: str</code><br>
<code>unk2: bool</code><br>
<code>unk3: int</code><br>
<code>mii_data: bytes</code><br>
</span><br>

## MiiList
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MiiList` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: str</code><br>
<code>unk2: bool</code><br>
<code>unk3: int</code><br>
<code>mii_datas: list[bytes]</code><br>
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
<code>datetime: [DateTime](common.md#datetime) = [DateTime](common.md#datetime).never()</code><br>
</span><br>

## MyProfile
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `MyProfile` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>region: int</code><br>
<code>country: int</code><br>
<code>area: int</code><br>
<code>language: int</code><br>
<code>platform: int</code><br>
<code>unk1: int</code><br>
<code>unk2: str</code><br>
<code>unk3: str</code><br>
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
<code>birthday: [DateTime](common.md#datetime)</code><br>
<code>unk: int</code><br>
</span><br>

## NintendoPresence
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `NintendoPresence` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>changed_bit_flag: int</code><br>
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>game_mode_description: str</code><br>
<code>join_availability_flag: int</code><br>
<code>matchmake_system_type: int</code><br>
<code>join_game_id: int</code><br>
<code>join_game_mode: int</code><br>
<code>owner_pid: int</code><br>
<code>join_group_id: int</code><br>
<code>application_data: bytes</code><br>
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

## PlayedGame
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PlayedGame` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>datetime: [DateTime](common.md#datetime)</code><br>
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
<code>show_online_status: bool</code><br>
<code>show_current_title: bool</code><br>
<code>block_friend_requests: bool</code><br>
</span><br>

## PrincipalRequestBlockSetting
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PrincipalRequestBlockSetting` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
<code>unk2: bool</code><br>
</span><br>

