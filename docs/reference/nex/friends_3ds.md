
# Module: <code>nintendo.nex.friends_3ds</code>

Provides a client and server for the `FriendsProtocolV1`. This page was generated automatically from `friends_3ds.proto`.

<code>**class** [FriendsClientV1](#friendsclientv1)</code><br>
<span class="docs">The client for the `FriendsProtocolV1`.</span>

<code>**class** [FriendsServerV1](#friendsserverv1)</code><br>
<span class="docs">The server for the `FriendsProtocolV1`.</span>

<code>**class** [FriendMii](#friendmii)([Structure](common.md))</code><br>
<code>**class** [FriendMiiList](#friendmiilist)([Structure](common.md))</code><br>
<code>**class** [FriendMiiRequest](#friendmiirequest)([Structure](common.md))</code><br>
<code>**class** [FriendPersistentInfo](#friendpersistentinfo)([Structure](common.md))</code><br>
<code>**class** [FriendPicture](#friendpicture)([Structure](common.md))</code><br>
<code>**class** [FriendPresence](#friendpresence)([Structure](common.md))</code><br>
<code>**class** [FriendRelationship](#friendrelationship)([Structure](common.md))</code><br>
<code>**class** [GameKey](#gamekey)([Data](common.md))</code><br>
<code>**class** [Mii](#mii)([Structure](common.md))</code><br>
<code>**class** [MiiList](#miilist)([Structure](common.md))</code><br>
<code>**class** [MyProfile](#myprofile)([Structure](common.md))</code><br>
<code>**class** [NintendoPresence](#nintendopresence)([Structure](common.md))</code><br>
<code>**class** [PlayedGame](#playedgame)([Structure](common.md))</code><br>

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

<code>**async def get_friend_mii**(friends: list[[FriendMiiRequest](#friendmiirequest)]) -> list[[FriendMii](#friendmii)]</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def get_friend_mii_list**(friends: list[[FriendMiiRequest](#friendmiirequest)]) -> list[[FriendMiiList](#friendmiilist)]</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def get_friend_relationships**(unk: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def add_friend_by_principal_id**(unk: int, pid: int) -> [FriendRelationship](#friendrelationship)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def get_all_friends**() -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def sync_friend**(unk1: int, unk2: list[int], unk3: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def update_presence**(presence_info: [NintendoPresence](#nintendopresence), unk: bool) -> None</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def update_favorite_game_key**(game_key: [GameKey](#gamekey)) -> None</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def update_comment**(comment: str) -> None</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def get_friend_presence**(unk: list[int]) -> list[[FriendPresence](#friendpresence)]</code><br>
<span class="docs">Calls method `22` on the server.</span>

<code>**async def get_friend_picture**(unk: list[int]) -> list[[FriendPicture](#friendpicture)]</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def get_friend_persistent_info**(unk: list[int]) -> list[[FriendPersistentInfo](#friendpersistentinfo)]</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def send_invitation**(unk: list[int]) -> None</code><br>
<span class="docs">Calls method `26` on the server.</span>

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

<code>**async def get_friend_mii**(client: [RMCClient](rmc.md#rmcclient), friends: list[[FriendMiiRequest](#friendmiirequest)]) -> list[[FriendMii](#friendmii)]</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_mii_list**(client: [RMCClient](rmc.md#rmcclient), friends: list[[FriendMiiRequest](#friendmiirequest)]) -> list[[FriendMiiList](#friendmiilist)]</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_relationships**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def add_friend_by_principal_id**(client: [RMCClient](rmc.md#rmcclient), unk: int, pid: int) -> [FriendRelationship](#friendrelationship)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def get_all_friends**(client: [RMCClient](rmc.md#rmcclient)) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def sync_friend**(client: [RMCClient](rmc.md#rmcclient), unk1: int, unk2: list[int], unk3: list[int]) -> list[[FriendRelationship](#friendrelationship)]</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def update_presence**(client: [RMCClient](rmc.md#rmcclient), presence_info: [NintendoPresence](#nintendopresence), unk: bool) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def update_favorite_game_key**(client: [RMCClient](rmc.md#rmcclient), game_key: [GameKey](#gamekey)) -> None</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def update_comment**(client: [RMCClient](rmc.md#rmcclient), comment: str) -> None</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_presence**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPresence](#friendpresence)]</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_picture**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPicture](#friendpicture)]</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def get_friend_persistent_info**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> list[[FriendPersistentInfo](#friendpersistentinfo)]</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def send_invitation**(client: [RMCClient](rmc.md#rmcclient), unk: list[int]) -> None</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

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

## FriendMiiRequest
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `FriendMiiRequest` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>unk1: int</code><br>
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

## PlayedGame
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `PlayedGame` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>game_key: [GameKey](#gamekey) = [GameKey](#gamekey)()</code><br>
<code>datetime: [DateTime](common.md#datetime)</code><br>
</span><br>

