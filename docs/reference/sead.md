
# Module: <code>nintendo.sead</code>

Implements the random number generator of the `sead` library. The random number generator uses a simple version of the Mersenne Twister algorithm, with only four 32-bit words of internal state.

<code>**class** [Random](#random)</code><br>
<span class="docs">The random number generator.</span>

## Random
<code>**def _\_init__**(seed: int)</code><br>
<span class="docs">Creates a new random number generator with the given seed.</span>

<code>**def _\_init__**(s0: int, s1: int, s2: int, s3: int)</code><br>
<span class="docs">Creates a new random number generator with the given internal state.</span>

<code>**def set_seed**(seed: int) -> None</code><br>
<span class="docs">Reinitializes the random number generator with the given seed.</span>

<code>**def set_state**(s0: int, s1: int, s2: int, s3: int) -> None</code><br>
<span class="docs">Reinitializes the random number generator with the given internal state.</span>

<code>**def u32**() -> int</code><br>
<span class="docs">Generates a random unsigned 32-bit integer</span>

<code>**def uint**(max: int) -> int </code><br>
<span class="docs">Generates a random unsigned integer between `0` and `max - 1`.
