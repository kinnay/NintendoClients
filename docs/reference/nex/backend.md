
# Module: <code>nintendo.nex.backend</code>

Provides a client for game servers.

<code>**class** [BackEndClient](#backendclient)</code><br>
<span class="docs">The game server client.</span>

<code>**async with connect**(settings: [Settings](../settings#settings), host: str, port: int) -> [BackEndClient](#backendclient)</code><br>
<span class="docs">Establishes a connection with the authentication server at the given address. Blocks until the connection is ready.</span>

## BackEndClient
<code>auth_client: [RMCClient](../rmc#rmcclient)</code><br>
<span class="docs">The RMC client that is connected to the authentication server.</span>

<code>**async with login**(username: str, password: str = None, auth_info: [Data](../common) = None, servers: list[object] = []) -> [RMCClient](../rmc#rmcclient)</code><br>
<span class="docs">Requests a ticket from the authentication server and establishes a connection with the secure server. The returned RMC client can be used to call methods on the secure server. `servers` must be a list of protocol server objects that should be defined in an external protocol file. These servers are registered on the secure client.</span>

<code>**async with login_guest**() -> [RMCClient](../rmc#rmcclient)</code><br>
<span class="docs">Logs in as guest. On most servers the guest account is disabled.</span>
