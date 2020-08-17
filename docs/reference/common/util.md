
# Module: <code>nintendo.common.util</code>

Provides useful functions that didn't fit into another module.

<code>**def is_hexadecimal**(s: str) -> bool</code><br>
<span class="docs">Returns `True` if `s` is non-empty and only contains hexadecimal digits.</span>

<code>**def ip_to_hex**(ip: str) -> int</code><br>
<span class="docs">Converts an IPv4 address string to an integer in big-endian byte order. Raises `ValueError` if the IP address is invalid.</span>

<code>**def ip_from_hex**(value: int) -> str</code><br>
<span class="docs">Converts an integer to an IPv4 addresses string in big-endian byte order.</span>

<code>**def local_address**() -> str</code><br>
<span class="docs">Returns the local IPv4 address of the default interface. Raises `ConnectionError` if no IPv4 interface was found.</span>

<code>**def broadcast_address**() -> str</code><br>
<span class="docs">Returns the IPv4 broadcast address of the default interface. Raises `ConnectionError` if no IPv4 interface was found.</span>
