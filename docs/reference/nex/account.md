
# Module: <code>nintendo.nex.account</code>

Provides a client and server for the `AccountProtocol`. This page was generated automatically from `account.proto`.

<code>**class** [AccountClient](#accountclient)</code><br>
<span class="docs">The client for the `AccountProtocol`.</span>

<code>**class** [AccountServer](#accountserver)</code><br>
<span class="docs">The server for the `AccountProtocol`.</span>

<code>**class** [AccountData](#accountdata)([Structure](../common))</code><br>
<code>**class** [BasicAccountInfo](#basicaccountinfo)([Structure](../common))</code><br>

## AccountClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`AccountClient`](#accountclient).</span>

<code>**async def create_account**(name: str, key: str, groups: int, email: str) -> [Result](../common#result)</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def delete_account**(pid: int) -> None</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def disable_account**(pid: int, until: [DateTime](../common#datetime), message: str) -> [Result](../common#result)</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def change_password**(new_key: str) -> bool</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def test_capability**(capability: int) -> bool</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def get_name**(pid: int) -> str</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def get_account_data**() -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `7` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>data: [AccountData](#accountdata)</code><br>
</span>
</span>

<code>**async def get_private_data**() -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `8` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: [Data](../common)</code><br>
</span>
</span>

<code>**async def get_public_data**(pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `9` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: [Data](../common)</code><br>
</span>
</span>

<code>**async def get_multiple_public_data**(pids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `10` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: list[[Data](../common)]</code><br>
</span>
</span>

<code>**async def update_account_name**(name: str) -> [Result](../common#result)</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def update_account_email**(email: str) -> [Result](../common#result)</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def update_custom_data**(public_data: [Data](../common), private_data: [Data](../common)) -> [Result](../common#result)</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def find_by_name_regex**(groups: int, regex: str, range: [ResultRange](../common#resultrange)) -> list[[BasicAccountInfo](#basicaccountinfo)]</code><br>
<span class="docs">Calls method `14` on the server.</span>

<code>**async def update_account_expiry_date**(pid: int, expiry: [DateTime](../common#datetime), message: str) -> None</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def update_account_effective_date**(pid: int, effective_from: [DateTime](../common#datetime), message: str) -> None</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def update_status**(status: str) -> None</code><br>
<span class="docs">Calls method `17` on the server.</span>

<code>**async def get_status**(pid: int) -> str</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def get_last_connection_stats**(pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `19` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>last_session_login: [DateTime](../common#datetime)</code><br>
<code>last_session_logout: [DateTime](../common#datetime)</code><br>
<code>current_session_login: [DateTime](../common#datetime)</code><br>
</span>
</span>

<code>**async def reset_password**() -> bool</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def create_account_with_custom_data**(name: str, key: str, groups: int, email: str, public_data: [Data](../common), private_data: [Data](../common)) -> None</code><br>
<span class="docs">Calls method `21` on the server.</span>

<code>**async def retrieve_account**() -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `22` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>account_data: [AccountData](#accountdata)</code><br>
<code>public_data: [Data](../common)</code><br>
<code>private_data: [Data](../common)</code><br>
</span>
</span>

<code>**async def update_account**(key: str, email: str, public_data: [Data](../common), private_data: [Data](../common)) -> None</code><br>
<span class="docs">Calls method `23` on the server.</span>

<code>**async def change_password_by_guest**(name: str, email: str, key: str) -> None</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def find_by_name_like**(groups: int, like: str, range: [ResultRange](../common#resultrange)) -> list[[BasicAccountInfo](#basicaccountinfo)]</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def custom_create_account**(name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> int</code><br>
<span class="docs">Calls method `26` on the server.</span>

<code>**async def nintendo_create_account**(name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `27` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>pid: int</code><br>
<code>pid_hmac: str</code><br>
</span>
</span>

<code>**async def lookup_or_create_account**(name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> int</code><br>
<span class="docs">Calls method `28` on the server.</span>

<code>**async def disconnect_principal**(pid: int) -> bool</code><br>
<span class="docs">Calls method `29` on the server.</span>

<code>**async def disconnect_all_principals**() -> bool</code><br>
<span class="docs">Calls method `30` on the server.</span>

## AccountServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`AccountServer`](#accountserver).</span>

<code>**def process_event**(type: int, client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called when a [client event](../rmc#rmcevent) occurs. May be overridden by a subclass.</span>

<code>**async def create_account**(client: [RMCClient](../rmc#rmcclient), name: str, key: str, groups: int, email: str) -> [Result](../common#result)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def delete_account**(client: [RMCClient](../rmc#rmcclient), pid: int) -> None</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def disable_account**(client: [RMCClient](../rmc#rmcclient), pid: int, until: [DateTime](../common#datetime), message: str) -> [Result](../common#result)</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def change_password**(client: [RMCClient](../rmc#rmcclient), new_key: str) -> bool</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def test_capability**(client: [RMCClient](../rmc#rmcclient), capability: int) -> bool</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def get_name**(client: [RMCClient](../rmc#rmcclient), pid: int) -> str</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def get_account_data**(client: [RMCClient](../rmc#rmcclient)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: [Result](../common#result)</code><br>
<code>data: [AccountData](#accountdata)</code><br>
</span>
</span>

<code>**async def get_private_data**(client: [RMCClient](../rmc#rmcclient)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: [Data](../common)</code><br>
</span>
</span>

<code>**async def get_public_data**(client: [RMCClient](../rmc#rmcclient), pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: [Data](../common)</code><br>
</span>
</span>

<code>**async def get_multiple_public_data**(client: [RMCClient](../rmc#rmcclient), pids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: bool</code><br>
<code>data: list[[Data](../common)]</code><br>
</span>
</span>

<code>**async def update_account_name**(client: [RMCClient](../rmc#rmcclient), name: str) -> [Result](../common#result)</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def update_account_email**(client: [RMCClient](../rmc#rmcclient), email: str) -> [Result](../common#result)</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def update_custom_data**(client: [RMCClient](../rmc#rmcclient), public_data: [Data](../common), private_data: [Data](../common)) -> [Result](../common#result)</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def find_by_name_regex**(client: [RMCClient](../rmc#rmcclient), groups: int, regex: str, range: [ResultRange](../common#resultrange)) -> list[[BasicAccountInfo](#basicaccountinfo)]</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass.</span>

<code>**async def update_account_expiry_date**(client: [RMCClient](../rmc#rmcclient), pid: int, expiry: [DateTime](../common#datetime), message: str) -> None</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def update_account_effective_date**(client: [RMCClient](../rmc#rmcclient), pid: int, effective_from: [DateTime](../common#datetime), message: str) -> None</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def update_status**(client: [RMCClient](../rmc#rmcclient), status: str) -> None</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass.</span>

<code>**async def get_status**(client: [RMCClient](../rmc#rmcclient), pid: int) -> str</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def get_last_connection_stats**(client: [RMCClient](../rmc#rmcclient), pid: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>last_session_login: [DateTime](../common#datetime)</code><br>
<code>last_session_logout: [DateTime](../common#datetime)</code><br>
<code>current_session_login: [DateTime](../common#datetime)</code><br>
</span>
</span>

<code>**async def reset_password**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def create_account_with_custom_data**(client: [RMCClient](../rmc#rmcclient), name: str, key: str, groups: int, email: str, public_data: [Data](../common), private_data: [Data](../common)) -> None</code><br>
<span class="docs">Handler for method `21`. This method should be overridden by a subclass.</span>

<code>**async def retrieve_account**(client: [RMCClient](../rmc#rmcclient)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>account_data: [AccountData](#accountdata)</code><br>
<code>public_data: [Data](../common)</code><br>
<code>private_data: [Data](../common)</code><br>
</span>
</span>

<code>**async def update_account**(client: [RMCClient](../rmc#rmcclient), key: str, email: str, public_data: [Data](../common), private_data: [Data](../common)) -> None</code><br>
<span class="docs">Handler for method `23`. This method should be overridden by a subclass.</span>

<code>**async def change_password_by_guest**(client: [RMCClient](../rmc#rmcclient), name: str, email: str, key: str) -> None</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def find_by_name_like**(client: [RMCClient](../rmc#rmcclient), groups: int, like: str, range: [ResultRange](../common#resultrange)) -> list[[BasicAccountInfo](#basicaccountinfo)]</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def custom_create_account**(client: [RMCClient](../rmc#rmcclient), name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> int</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

<code>**async def nintendo_create_account**(client: [RMCClient](../rmc#rmcclient), name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `27`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>pid: int</code><br>
<code>pid_hmac: str</code><br>
</span>
</span>

<code>**async def lookup_or_create_account**(client: [RMCClient](../rmc#rmcclient), name: str, key: str, groups: int, email: str, auth_data: [Data](../common)) -> int</code><br>
<span class="docs">Handler for method `28`. This method should be overridden by a subclass.</span>

<code>**async def disconnect_principal**(client: [RMCClient](../rmc#rmcclient), pid: int) -> bool</code><br>
<span class="docs">Handler for method `29`. This method should be overridden by a subclass.</span>

<code>**async def disconnect_all_principals**(client: [RMCClient](../rmc#rmcclient)) -> bool</code><br>
<span class="docs">Handler for method `30`. This method should be overridden by a subclass.</span>

## AccountData
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `AccountData` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>name: str</code><br>
<code>groups: int</code><br>
<code>email: str</code><br>
<code>creation_date: [DateTime](../common#datetime)</code><br>
<code>effective_date: [DateTime](../common#datetime)</code><br>
<code>not_effective_message: str</code><br>
<code>expiry_date: [DateTime](../common#datetime)</code><br>
<code>expired_message: str</code><br>
</span><br>

## BasicAccountInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BasicAccountInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>pid: int</code><br>
<code>name: str</code><br>
</span><br>

