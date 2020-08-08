
# Module: <code>nintendo.common.streams</code>

Provides classes to parse and build files in a stream-like fashion.

<code>**class** [StreamOut](#streamout)</code><br>
<span class="docs">A byte stream that writes to a memory buffer.</span>

<code>**class** [StreamIn](#streamout)</code><br>
<span class="docs">A byte stream that reads from a memory buffer.</span>

<code>**class** [BitStreamOut](#bitstreamout)([StreamOut](#streamout))</code><br>
<span class="docs">An output stream that can write individual bits.</span>

<code>**class** [BitStreamIn](#bitstreamin)([StreamIn](#streamin))</code><br>
<span class="docs">An input stream that can read individual bits.</span>

## StreamOut
<code>**def _\_init__**(endian: str = "<")</code><br>
<span class="docs">Creates a new output stream with an empty memory buffer. `endian` should be either `"<"` (little-endian) or `">"` (big-endian).</span>

<code>**def push**() -> None</code><br>
<span class="docs">Saves the current stream position on a stack.</span>

<code>**def pop**() -> None</code><br>
<span class="docs">Restores the old stream position from the stack.</span>

<code>**def get**() -> bytes</code><br>
<span class="docs">Returns a copy of the memory buffer.</span>

<code>**def size**() -> int</code><br>
<span class="docs">Returns the size of the current memory buffer in bytes.</span>

<code>**def tell**() -> int</code><br>
<span class="docs">Returns the current position of the stream in bytes.</span>

<code>**def seek**(int: pos) -> None</code><br>
<span class="docs">Moves the stream to a different position in bytes. If the stream is moved past the end of the current memory buffer it is filled with null bytes up to the given `pos`.</span>

<code>**def skip**(int: num) -> None</code><br>
<span class="docs">Increases the stream position by `num` bytes. If the stream is moved past the end of the current memory buffer it is filled with null bytes up to the new position.</span>

<code>**def align**(int: num) -> None</code><br>
<span class="docs">Makes sure that the stream position is a multiple of `num` bytes (increasing it if necessary). If the stream is moved past the end of the current memory buffer it is filled with null bytes up to the new position.</span>

<code>**def available**() -> int</code><br>
<span class="docs">Returns the number of bytes between the current stream position and the end of the current memory buffer.</span>

<code>**def eof**() -> bool</code><br>
<span class="docs">Returns `True` if the stream points at the end of the current memory buffer.</span>

<code>**def write**(data: bytes) -> None</code><br>
<span class="docs">Writes data into the memory buffer and increases the stream position.</span>

<code>**def pad**(num: int, char: bytes = b"\0") -> None</code><br>
<span class="docs">Writes `num` copies of `char` into the stream.</span>

<code>**def ascii**(data: str) -> None</code><br>
<span class="docs">Writes an ascii string into the stream (without null terminator).</span>

<code>**def u8**(value: int) -> None</code><br>
<span class="docs">Writes an unsigned 8-bit integer into the stream.</span>

<code>**def u16**(value: int) -> None</code><br>
<span class="docs">Writes an unsigned 16-bit integer into the stream.</span>

<code>**def u24**(value: int) -> None</code><br>
<span class="docs">Writes an unsigned 24-bit integer into the stream.</span>

<code>**def u32**(value: int) -> None</code><br>
<span class="docs">Writes an unsigned 32-bit integer into the stream.</span>

<code>**def u64**(value: int) -> None</code><br>
<span class="docs">Writes an unsigned 64-bit integer into the stream.</span>

<code>**def s8**(value: int) -> None</code><br>
<span class="docs">Writes a signed 8-bit integer into the stream.</span>

<code>**def s16**(value: int) -> None</code><br>
<span class="docs">Writes a signed 16-bit integer into the stream.</span>

<code>**def s32**(value: int) -> None</code><br>
<span class="docs">Writes a signed 32-bit integer into the stream.</span>

<code>**def s64**(value: int) -> None</code><br>
<span class="docs">Writes a signed 64-bit integer into the stream.</span>

<code>**def float**(value: float) -> None</code><br>
<span class="docs">Writes a 32-bit float into the stream.</span>

<code>**def double**(value: float) -> None</code><br>
<span class="docs">Writes a 64-bit float into the stream.</span>

<code>**def bool**(value: bool) -> None</code><br>
<span class="docs">Writes a bool into the stream as an 8-bit integer (either 0 or 1).</span>

<code>**def char**(value: str) -> None</code><br>
<span class="docs">Writes a single 8-bit unicode character into the stream.</span>

<code>**def wchar**(value: str) -> None</code><br>
<span class="docs">Writes a single 16-bit unicode character into the stream.</span>

<code>**def chars**(value: str) -> None</code><br>
<span class="docs">Writes a string of 8-bit unicode characters into the stream.</span>

<code>**def wchars**(value: str) -> None</code><br>
<span class="docs">Writes a string of 16-bit unicode characters into the stream.</span>

<code>**def repeat**(list: list, func: Callable) -> None</code><br>
<span class="docs">Invokes `func` on every item in `list`. This function can be used to write a list of values into the stream. For example: `stream.repeat([1, 2, 3], stream.u8)`.</span>

## StreamIn
Any operation that moves the stream position past the end of the buffer raises `OverflowError`.

<code>**def _\_init__**(data: bytes, endian: str = "<")</code><br>
<span class="docs">Creates a new input stream from the given memory buffer. `endian` should be either `"<"` (little-endian) or `">"` (big-endian).</span>

<code>**def push**() -> None</code><br>
<span class="docs">Saves the current stream position on a stack.</span>

<code>**def pop**() -> None</code><br>
<span class="docs">Restores the old stream position from the stack.</span>

<code>**def get**() -> bytes</code><br>
<span class="docs">Returns the whole memory buffer.</span>

<code>**def size**() -> int</code><br>
<span class="docs">Returns the size of the memory buffer in bytes.</span>

<code>**def tell**() -> int</code><br>
<span class="docs">Returns the current position of the stream in bytes.</span>

<code>**def seek**(int: pos) -> None</code><br>
<span class="docs">Moves the stream to a different position in bytes.</span>

<code>**def skip**(int: num) -> None</code><br>
<span class="docs">Increases the stream position by `num` bytes.</span>

<code>**def align**(int: num) -> None</code><br>
<span class="docs">Makes sure that the stream position is a multiple of `num` bytes (increasing it if necessary).</span>

<code>**def available**() -> int</code><br>
<span class="docs">Returns the number of bytes between the current stream position and the end of the memory buffer.</span>

<code>**def eof**() -> bool</code><br>
<span class="docs">Returns `True` if the stream points at the end of the memory buffer.</span>

<code>**def peek**(num: int) -> bytes</code><br>
<span class="docs">Reads `num` bytes from the memory buffer without advancing the stream pointer. Raises `OverflowError` if less than `num` bytes are available.</span>

<code>**def read**(num: int) -> bytes</code><br>
<span class="docs">Reads `num` bytes from the memory buffer and advances the stream pointer accordingly.</span>

<code>**def readall**() -> bytes</code><br>
<span class="docs">Reads all remaining bytes from the memory buffer.</span>

<code>**def pad**(num: int, char: bytes = b"\0") -> None</code><br>
<span class="docs">Consumes `num` bytes from the memory buffer and makes sure that they are equal to `char`. Raises `ValueError` if any of the bytes is not equal to `char`.</span>

<code>**def ascii**(num: int) -> str</code><br>
<span class="docs">Reads an ascii string from the stream of `num` bytes.</span>

<code>**def u8**() -> int</code><br>
<span class="docs">Reads an unsigned 8-bit integer from the stream.</span>

<code>**def u16**() -> int</code><br>
<span class="docs">Reads an unsigned 16-bit integer from the stream.</span>

<code>**def u24**() -> int</code><br>
<span class="docs">Reads an unsigned 24-bit integer from the stream.</span>

<code>**def u32**() -> int</code><br>
<span class="docs">Reads an unsigned 32-bit integer from the stream.</span>

<code>**def u64**() -> int</code><br>
<span class="docs">Reads an unsigned 64-bit integer from the stream.</span>

<code>**def s8**() -> int</code><br>
<span class="docs">Reads a signed 8-bit integer from the stream.</span>

<code>**def s16**() -> int</code><br>
<span class="docs">Reads a signed 16-bit integer from the stream.</span>

<code>**def s32**() -> int</code><br>
<span class="docs">Reads a signed 32-bit integer from the stream.</span>

<code>**def s64**() -> int</code><br>
<span class="docs">Reads a signed 64-bit integer from the stream.</span>

<code>**def float**() -> float</code><br>
<span class="docs">Reads a 32-bit float from the stream.</span>

<code>**def double**() -> float</code><br>
<span class="docs">Reads a 64-bit float from the stream.</span>

<code>**def bool**() -> bool</code><br>
<span class="docs">Reads an 8-bit integer from the stream. Returns `True` if the integer is non-zero.</span>

<code>**def char**() -> str</code><br>
<span class="docs">Reads an 8-bit unicode character from the stream.</span>

<code>**def wchar**() -> str</code><br>
<span class="docs">Reads a 16-bit unicode character from the stream.</span>

<code>**def chars**(num: int) -> str</code><br>
<span class="docs">Reads `num` 8-bit unicode characters from the stream.</span>

<code>**def wchars**(num: int) -> str</code><br>
<span class="docs">Reads `num` 16-bit unicode characters from the stream.</span>

<code>**def repeat**(func: Callable, num: int) -> list</code><br>
<span class="docs">Invokes `func` exactly `num` times and returns its return values as a list. This function can be used to read a list of values from the stream. For example: `values = stream.repeat(stream.u8, 10)`</span>

## BitStreamOut
This class inherits [`StreamOut`](#streamout). All regular functions are still supported. However, writes are much faster if the stream is byte aligned.

<code>**def seekbits**(pos: int) -> None</code><br>
<span class="docs">Moves the stream to a different position in bits.</span>

<code>**def tellbits**() -> int</code><br>
<span class="docs">Returns the current position of the stream in bits</span>

<code>**def bytealign**() -> None</code><br>
<span class="docs">Ensures that stream points to the start of a byte. If the stream points into the middle of a byte it is moved to the next byte.</span>

<code>**def bit**(value: int) -> None</code><br>
<span class="docs">Writes a single bit into the stream.</span>

<code>**def bits**(value: int, num: int) -> None</code><br>
<span class="docs">Writes an unsigned integer of `num` bits into the stream in big-endian bit and byte order.</span>

## BitStreamIn
This class inherits [`StreamIn`](#streamin). All regular functions are still supported. However, reads are much faster if the stream is byte aligned.

<code>**def seekbits**(pos: int) -> None</code><br>
<span class="docs">Moves the stream to a different position in bits.</span>

<code>**def tellbits**() -> int</code><br>
<span class="docs">Returns the current position of the stream in bits</span>

<code>**def bytealign**() -> None</code><br>
<span class="docs">Ensures that stream points to the start of a byte. If the stream points into the middle of a byte it is moved to the next byte.</span>

<code>**def bit**() -> int</code><br>
<span class="docs">Reads a single bit from the stream.</span>

<code>**def bits**(num: int) -> int</code><br>
<span class="docs">Reads an unsigned integer of `num` bits from the stream in big-endian bit and byte order.</span>
