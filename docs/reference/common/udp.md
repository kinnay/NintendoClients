
# Module: <code>nintendo.common.udp</code>

Provides a UDP socket, client and server.

<code>**class** [UDPSocket](#udpsocket)</code><br>
<span class="docs">A connectionless UDP socket.</span>

<code>**class** [UDPClient](#udpclient)</code><br>
<span class="docs">UDP socket that is connected to a specific address.</span>

<code>**async with bind**(host: str = "", port: int = 0) -> [UDPSocket](#udpsocket)</code><br>
<span class="docs">Creates a UDP socket and binds it to the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system.</span>

<code>**async with connect**(host: str, port: int) -> [UDPClient](#udpclient)</code><br>
<span class="docs">Creates a UDP socket and connects it to the given address, i.e. all datagrams are sent to this address and datagrams that come from a different address are discarded.</span>

<code>**async with serve**(handler: Callable, host: str = "", port: int = 0) -> None</code><br>
<span class="docs">Creates a UDP server and binds it to the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system. `handler` must be an `async` function that accepts a [`UDPClient`](#udpclient). The client is closed automatically when `handler` returns.</span>

## UDPSocket
<code>**async def send**(data: bytes, addr: tuple[str, int]) -> None</code><br>
<span class="docs">Sends a datagram to the given address.</span>

<code>**async def recv**(num: int = 65536) -> (bytes, tuple[str, int])</code><br>
<span class="docs">Receives a single datagram of at most `num` bytes. Blocks if no datagram is available.</span>

<code>**async def close**() -> None</code><br>
<span class="docs">Closes the socket. If the socket is wrapped in an `async with` statement it is closed automatically.</span>

<code>**async def abort**() -> None</code><br>
<span class="docs">Same as `close`.</span>

<code>**async def broadcast**(data: bytes, port: int) -> None</code><br>
<span class="docs">Sends a datagram to the broadcast address of the default interface.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the socket.</span>

## UDPClient
<code>**async def send**(data: bytes) -> None</code><br>
<span class="docs">Sends a single datagram to the server.</span>

<code>**async def recv**(num: int = 65536) -> bytes</code><br>
<span class="docs">Receives a single datagram of at most `num` bytes. Blocks if no datagram is available.</span>

<code>**async def close**() -> None</code><br>
<span class="docs">Closes the client. If the client is wrapped in an `async with` statement it is closed automatically.</span>

<code>**async def abort**() -> None</code><br>
<span class="docs">Same as `close`.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the client.</span>

<code>**def remote_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address that the client is connected to.</span>