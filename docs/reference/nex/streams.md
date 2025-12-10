
# Module: <code>nintendo.nex.streams</code>

Extends [generic memory streams](https://anynet.readthedocs.io/en/latest/reference/streams) with useful `nex` related methods.

<code>**class** StreamOut([anynet.StreamOut](https://anynet.readthedocs.io/en/latest/reference/streams/#streamout))</code><br>
<span class="docs">An output stream that supports various `nex` structures.</span>

<code>**class** StreamIn([anynet.StreamIn](https://anynet.readthedocs.io/en/latest/reference/streams/#streamin))</code><br>
<span class="docs">An input stream that supports various `nex` structures.</span>

## StreamOut
<code>**def _\_init__**(settings: [Settings](settings.md#settings))</code><br>
<span class="docs">Creates a new output stream.</span>

<code>**def pid**(value: int) -> None</code><br>
<span class="docs">Writes a user id into the stream.</span>

<code>**def result**(value: [Result](common.md#result)) -> None</code><br>
<span class="docs">Writes a result into the stream.</span>

<code>**def list**(value: list, func: Callable) -> None</code><br>
<span class="docs">Writes a list into the stream. For example: `stream.list([1, 2, 3], stream.u8)`.</span>

<code>**def map**(value: dict, keyfunc: Callable, valuefunc: Callable) -> None</code><br>
<span class="docs">Writes a map into the stream. For example: `stream.map({"a": 1, "b": 2}, stream.string, stream.u8)`.</span>

<code>**def string**(value: str) -> None</code><br>
<span class="docs">Writes an UTF-8 string into the stream. Automatically adds a null terminator.</span>

<code>**def stationurl**(value: [StationURL](common.md#stationurl)) -> None</code><br>
<span class="docs">Writes a [StationURL](common.md#stationurl) into the stream.</span>

<code>**def datetime**(value: [DateTime](common.md#datetime)) -> None</code><br>
<span class="docs">Writes a [DateTime](common.md#datetime) object into the stream.</span>

<code>**def buffer**(value: bytes) -> None</code><br>
<span class="docs">Writes a buffer into the stream with a 32-bit length field.</span>

<code>**def qbuffer**(value: bytes) -> None</code><br>
<span class="docs">Writes a buffer into the stream with a 16-bit length field.</span>

<code>**def add**(value: [Structure](common.md)) -> None</code><br>
<span class="docs">Writes a `nex` structure into the stream.</span>

<code>**def anydata**(value: object) -> None</code><br>
<span class="docs">Wraps a structure in a data holder and writes it into the stream.</span>

<code>**def variant**(value: object) -> None</code><br>
<span class="docs">Writes a variant into the stream. `value` must be either `None` or an instance of `int`, `float`, `bool`, `str` or [`DateTime`](common.md#datetime).</span>

## StreamIn
<code>**def _\_init__**(data: bytes, settings: [Settings](settings.md#settings))</code><br>
<span class="docs">Creates a new input stream.</span>

<code>**def pid**() -> int</code><br>
<span class="docs">Reads a user id from the stream.</span>

<code>**def result**() -> [Result](common.md#result)</code><br>
<span class="docs">Reads a result from the stream.</span>

<code>**def repeat**(func: Callable, num: int) -> list</code><br>
<span class="docs">Extracts a fixed number of copies of a given type from the stream. For convenience, `func` may also be a subclass of [`Structure`](common.md) instead of a function. For example: `stream.repeat(stream.u8, 5)` or `stream.repeat(ResultRange, 2)`.</span>

<code>**def list**(func: Callable) -> list</code><br>
<span class="docs">Reads a list from the stream. For convenience, `func` may also be a subclass of [`Structure`](common.md) instead of a function. For example: `stream.list(stream.u8)` or `stream.list(ResultRange)`.</span>

<code>**def map**(keyfunc: Callable, valuefunc: Callable) -> dict</code><br>
<span class="docs">Reads a map from the stream. For convenience, `keyfunc` and `valuefunc` may also be a subclass of [`Structure`](common.md) instead of a function. For example: `stream.map(stream.string, ResultRange)`.</span>

<code>**def string**() -> str</code><br>
<span class="docs">Reads a UTF-8 string from the stream. Automatically removes the null terminator.</span>

<code>**def stationurl**() -> [StationURL](common.md#stationurl)</code><br>
<span class="docs">Reads a station url from the stream.</span>

<code>**def datetime**() -> [DateTime](common.md#datetime)</code><br>
<span class="docs">Reads a [DateTime](common.md#datetime) object from the stream.</span>

<code>**def buffer**() -> bytes</code><br>
<span class="docs">Reads a buffer from the stream with a 32-bit length field.</span>

<code>**def qbuffer**() -> bytes</code><br>
<span class="docs">Reads a buffer from the stream with a 16-bit length field.</span>

<code>**def substream**() -> [StreamIn](#streamin)</code><br>
<span class="docs">Reads a buffer from the stream with a 32-bit length field and returns an input stream.</span>

<code>**def extract**(cls: Type[[Structure](common.md)]) -> [Structure](common.md)</code><br>
<span class="docs">Reads a `nex` structure from the stream.</span>

<code>**def anydata**() -> object</code><br>
<span class="docs">Reads a data holder from the stream and returns its content, which is usually a subclass of [`Data`](common.md).</span>

<code>**def variant**() -> object</code><br>
<span class="docs">Reads a variant from the stream.</span>
