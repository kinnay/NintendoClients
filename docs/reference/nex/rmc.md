
# Module: <code>nintendo.nex.rmc</code>

Provides a client and server for the RMC protocol. An alternative client that calls remote methods through HTTP can be found in the [`nintendo.nex.hpp`](hpp.md) module.

<code>**class** RMCResponse</code><br>
<span class="docs">Generic response object that is returned when a remote method returns multiple values. The attributes depend on the method.</span>

<code>**class** [RMCClient](#rmcclient)</code><br>
<span class="docs">RMC client that uses a PRUDP connection.</span>

<code>**async with connect**(settings: [Settings](settings.md#settings), host: str, port: int, vport: int = 1, context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None, credentials: [Credentials](kerberos.md#credentials) = None, servers: list[object] = []) -> [RMCClient](#rmcclient)</code><br>
<span class="docs">Creates an RMC client based on PRUDP and connects it to the given address. If `context` is provided, and the underlying transport supports this, the connections is secured with TLS. If credentials are provided they are sent to the server in the connection request. Blocks until the connection is ready and handshake has been performed. `servers` must be a list of service implementations.</span>

<code>**async with serve**(settings: [Settings](settings.md#settings), servers: list[object], host: str = "", port: int = 0, vport: int = 1, context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None, key: bytes = None) -> None</code><br>
<span class="docs">Creates an RMC server based on PRUDP and binds it to the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system. If `context` is provided, and the underlying transport supports this, the server is secured with TLS. If `key` is provided it is used to decrypt the Kerberos tickets in connection requests. If `key` is `None`, the payload of connection requests is ignored and all client connections are accepted. `servers` must be a list of service implementations.</span>

<code>**async with serve_on_transport**(settings: [Settings](settings.md#settings), servers: list[object], transport: [PRUDPServerTransport](prudp.md#prudpservertransport), port: int, key: bytes = None) -> None</code><br>
<span class="docs">Creates an RMC server on top of the given transport server. If `key` is provided it is used to decrypt the Kerberos tickets in connection requests. If `key` is `None`, the payload of connection requests is ignored and all client connections are accepted. `servers` must be a list of service implementations.</span>

## RMCClient
<code>**async def request**(protocol: int, method: int, body: bytes, noresponse: bool = False) -> bytes</code><br>
<span class="docs">Performs a remote method call. Blocks until the RMC is complete. Returns the body of the RMC response on success. Raises [`RMCError`](common.md#rmcerror) if the server returns an error code.<br><br>If `noresponse` is `True`, this method does not wait for a response and returns `None` immediately.</span>

<code>**def pid**() -> int</code><br>
<span class="docs">Returns the user id of the connected client. Returns `None` if the client is connected without credentials.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the client.</span>

<code>**def remote_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address that the client is connected to.</span>

<code>**def local_sid**() -> int</code><br>
<span class="docs">Returns the local stream id (PRUDP port).</span>

<code>**def remote_sid**() -> int</code><br>
<span class="docs">Returns the remote stream id (PRUDP port).</span>
