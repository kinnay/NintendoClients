
# Module: <code>nintendo.enl.crypto</code>

Implements cryptographic operations used by the `enl` library.

<code>**def create_key**(rand: [sead.Random](../../sead#random), table: list[int], size: int)</code><br>
<span class="docs">Generates a random key of `size` bytes based on the given random number generator and integer table. `size` must be a multiple of four. See [here](https://github.com/Kinnay/NintendoClients/wiki/ENL-Key-Generation) for details on the algorithm.</span>
