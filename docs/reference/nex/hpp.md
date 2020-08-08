
# Module: <code>nintendo.nex.hpp</code>

Provides a client that performs remote method calls through HTTP.

<code>**class** [HppClient](#hppclient)</code><br>
<span class="docs">The HTTP RMC client.</span>

## HppClient
<code>**def _\_init__**(settings: [Settings](../../common/settings#settings), game_server_id: int, nex_version: str, pid: int, password: str)</code><br>
<span class="docs">Creates a new `hpp` client.</span>

<code>**def set_environment**(env: str) -> None</code><br>
<span class="docs">Changes the environment. The default is `"L1"` (production).</span><br>

<code>**async def request**(protocol: int, method: int, body: bytes) -> bytes</code><br>
<span class="docs">Performs a remote method call. Blocks until the RMC is complete. Returns the body of the RMC response on success. Raises [`RMCError`](../common#rmcerror) if the server returns an error code.</span>
