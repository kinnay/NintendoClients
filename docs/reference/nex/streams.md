
# Module: <code>nintendo.nex.streams</code>

Extends [generic memory streams](../../common/streams) with useful `nex` related methods.

<code>**class** StreamOut([common.StreamOut](../../common/streams#streamout))</code><br>
<span class="docs">An output stream that supports various `nex` structures.</span>

<code>**class** StreamIn([common.StreamIn](../../common/streams#streamin))</code><br>
<span class="docs">An input stream that supports various `nex` structures.</span>

## StreamOut
<code>**def _\_init__**(settings: [Settings](../../settings#settings))</code><br>
<span class="docs">Creates a new output stream.</span>

<code>**def pid**(value: int) -> None</code><br>
<span class="docs">Writes a user id into the stream.</span>

<code>**def result**(value: [Result](../common#result)) -> None</code><br>
<span class="docs">Writes a result into the stream.</span>

<code>**def list**(value: list, func: Callable) -> None</code><br>
<span class="docs">Writes a list into the stream. For example: `stream.list([1, 2, 3], stream.u8)`.</span>

<code>**def map**(value: dict, keyfunc: Callable, valuefunc: Callable) -> None</code><br>
<span class="docs">Writes a map into the stream. For example: `stream.map({"a": 1, "b": 2}, stream.string, stream.u8)`.</span>

<code>**def string**(value: str) -> None</code><br>
<span class="docs">Writes an UTF-8 string into the stream. Automatically adds a null terminator.</span>

<code>**def stationurl**(value: [StationURL](../common#stationurl)) -> None</code><br>
<span class="docs">Writes a [StationURL](../common#stationurl) into the stream.</span>

<code>**def datetime**(value: [DateTime](../common#datetime)) -> None</code><br>
<span class="docs">Writes a [DateTime](../common#datetime) object into the stream.</span>

<code>**def buffer**(value: bytes) -> None</code><br>
<span class="docs">Writes a buffer into the stream with a 32-bit length field.</span>

<code>**def qbuffer**(value: bytes) -> None</code><br>
<span class="docs">Writes a buffer into the stream with a 16-bit length field.</span>

<code>**def add**(value: [Structure](../common)) -> None</code><br>
<span class="docs">Writes a `nex` structure into the stream.</span>

<code>**def anydata**(value: [Data](../common)) -> None</code><br>
<span class="docs">Wraps a structure in a data holder and writes it into the stream.</span>

<code>**def variant**(value: object) -> None</code><br>
<span class="docs">Writes a variant into the stream. `value` must be either `None` or an instance of `int`, `float`, `bool`, `str` or [`DateTime`](../common#datetime).</span>

## StreamIn
<code>**def _\_init__**(data: bytes, settings: [Settings](../../settings#settings))</code><br>
<span class="docs">Creates a new input stream.</span>

<code>**def pid**() -> int</code><br>
<span class="docs">Reads a user id from the stream.</span>

<code>**def result**() -> [Result](../common#result)</code><br>
<span class="docs">Reads a result from the stream.</span>

<code>**def repeat**(func: Callable, num: int) -> list</code><br>
<span class="docs">Extracts a fixed number of copies of a given type from the stream. For convenience, `func` may also be a subclass of [`Structure`](../common) instead of a function. For example: `stream.repeat(stream.u8, 5)` or `stream.repeat(ResultRange, 2)`.</span>

<code>**def list**(func: Callable) -> list</code><br>
<span class="docs">Reads a list from the stream. For convenience, `func` may also be a subclass of [`Structure`](../common) instead of a function. For example: `stream.list(stream.u8)` or `stream.list(ResultRange)`.</span>

<code>**def map**(keyfunc: Callable, valuefunc: Callable) -> dict</code><br>
<span class="docs">Reads a map from the stream. For convenience, `keyfunc` and `valuefunc` may also be a subclass of [`Structure`](../common) instead of a function. For example: `stream.map(stream.string, ResultRange)`.</span>

<code>**def string**() -> str</code><br>
<span class="docs">Reads a UTF-8 string from the stream. Automatically removes the null terminator.</span>

<code>**def stationurl**() -> [StationURL](../common#stationurl)</code><br>
<span class="docs">Reads a station url from the stream.</span>

<code>**def datetime**() -> [DateTime](../common#datetime)</code><br>
<span class="docs">Reads a [DateTime](../common#datetime) object from the stream.</span>

<code>**def buffer**() -> bytes</code><br>
<span class="docs">Reads a buffer from the stream with a 32-bit length field.</span>

<code>**def qbuffer**() -> bytes</code><br>
<span class="docs">Reads a buffer from the stream with a 16-bit length field.</span>

<code>**def substream**() -> [StreamIn](#streamin)</code><br>
<span class="docs">Reads a buffer from the stream with a 32-bit length field and returns an input stream.</span>

<code>**def extract**(cls: Type[[Structure](../common)]) -> [Structure](../common)</code><br>
<span class="docs">Reads a `nex` structure from the stream.</span>

<code>**def anydata**() -> [Data](../common)</code><br>
<span class="docs">Reads a data holder from the stream and returns its [`Data`] object.</span>

<code>**def variant**() -> object</code><br>
<span class="docs">Reads a variant from the stream.</span>
