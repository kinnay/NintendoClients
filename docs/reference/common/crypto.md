
# Module: <code>nintendo.common.crypto</code>

Provides an implementation of the RC4 stream cipher.

<code>**class** [RC4](#Rc4)</code><br>
<span class="docs">An RC4 stream.</span>

## RC4
<code>**def _\_init__**(key: bytes, reset: bool = False)</code><br>
<span class="docs">Creates a new RC4 stream with the given key. If `reset` is `True`, the RC4 stream is reinitialized after every `crypt` operation.</span>

<code>**def set_key**(key: bytes) -> None</code><br>
<span class="docs">Changes the key and reinitializes the stream.</span>

<code>**def reset**() -> None</code><br>
<span class="docs">Resets the RC4 stream to its initial state.</span>

<code>**def crypt**(data: bytes) -> bytes</code><br>
<span class="docs">Applies the RC4 stream to the given data. Due to the nature of RC4, this function can be used for both encryption and decryption.
