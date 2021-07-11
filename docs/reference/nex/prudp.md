
# Module: <code>nintendo.nex.prudp</code>

Provides a client and server for PRUDP. Originally, PRUDP implemented reliable and secure transmission on top of UDP, but the Nintendo Switch introduced a 'Lite' mode in which PRUDP is implemented on top of TCP or WebSockets instead.

<code>**class** [PRUDPClient](#prudpclient)</code><br>
<span class="docs">A PRUDP client.</span>

<code>**async with connect**(settings: [Settings](settings.md#settings), host: str, port: int, vport: int = 1, type: int = 10, context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None, credentials: [Credentials](kerberos.md#credentials) = None) -> [PRUDPClient](#prudpclient)</code><br>
<span class="docs">Creates a PRUDP client and connects it to the given address. If `context` is provided, and the underlying transport supports this, the connections is secured with TLS. If credentials are provided they are sent to the server in the connection request. Blocks until the connection is ready and handshake has been performed.</code>

<code>**async with serve**(handler: Callable, settings: [Settings](settings.md#settings), host: str = "", port: int = 0, vport: int = 1, type: int = 10, context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None, key: bytes = None) -> None</code><br>
<span class="docs">Creates a PRUDP server and binds it to the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system. `handler` must be an `async` function that accepts a [`PRUDPClient`](#prudpclient). The client is closed automatically when `handler` returns. If `context` is provided, and the underlying transport supports this, the server is secured with TLS. If `key` is provided it is used to decrypt the Kerberos tickets in connection requests. If `key` is `None`, the payload of connection requests is ignored an all client connections are accepted.</span>

<code>**async with connect_transport**(settings: [Settings](settings.md#settings), host: str, port: int, context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None) -> [PRUDPClientTransport](#prudpclienttransport)</code><br>
<span class="docs">Creates a transport connection for the PRUDP protocol. This can be used to establish multiple PRUDP connections with a single socket.</span>

<code>**async with serve_transport**(settings: [Settings](settings.md#settings), host: str = "", port: int = 0, [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext) = None) -> [PRUDPServerTransport](#prudpservertransport)</code><br>
<span class="docs">Creates a transport server for the PRUDP protocol. This can be used to host multiple PRUDP servers at a single port.</span>

## PRUDPClient
<code>**async def send**(data: bytes, substream: int = 0) -> None</code><br>
<span class="docs">Sends a reliable data packet to the server through the given substream. Blocks if the send buffer is full. Packets are retransmitted automatically if no acknowledgement is received.</span>

<code>**async def send_unreliable**(data: bytes) -> None</code><br>
<span class="docs">Sends an unreliable data packet to the server. Blocks if the send buffer is full.</span><br>

<code>**async def recv**(substream: int = 0) -> bytes</code><br>
<span class="docs">Receives a single reliable data packet from the server from the given substream. Blocks if no reliable data is available.</span>

<code>**async def recv_unreliable**() -> bytes</code><br>
<span class="docs">Receives an unreliable data packet from the server. Blocks if no unreliable data is available.</span>

<code>**def pid**() -> int</code><br>
<span class="docs">Returns the user id of the connected client. Returns `None` if the client is connected without credentials.</span>

<code>**def minor_version**() -> int</code><br>
<span class="docs">Returns the PRUDP minor version that was negotiated during the handshake.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the client.</span>

<code>**def remote_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address that the client is connected to.</span>

<code>**def local_sid**() -> int</code><br>
<span class="docs">Returns the local stream id (PRUDP port).</span>

<code>**def remote_sid**() -> int</code><br>
<span class="docs">Returns the remote stream id (PRUDP port).</span>

## PRUDPClientTransport
<code>**async with connect**(port: int, type: int = 10, credentials: credentials: [Credentials](kerberos.md#credentials) = None) -> [PRUDPClient](#prudpclient)</code><br>
<span class="docs">Establishes a new PRUDP connection with the given PRUDP port.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the client.</span>

<code>**def remote_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address that the client is connected to.</span>

## PRUDPServerTransport
<code>**async with serve**(handler: Callable, port: int, type: int = 10, key: bytes = None) -> None</code><br>
<span class="docs">Creates a new PRUDP server at the given PRUDP port.</span>
