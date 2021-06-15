
# Module: <code>nintendo.nex.common</code>

Provides classes that are used by various `nex` modules.

<code>**class** [RMCError](#rmcerror)(Exception)</code><br>
<span class="docs">Raised when the server returns an error code.</span>

<code>**class** [Result](#result)</code><br>
<span class="docs">Holds the result of a remote method call.</span>

<code>**class** Structure</code><br>
<span class="docs">Base class for `nex` structures. This class should not be subclassed manually. Instead, structures should be defined in a protocol file.</span>

<code>**class** Data(Structure)</code><br>
<span class="docs">Base class for structures that can be held by a data holder. This class should not be subclassed manually. Instead, data structures should be defined in a protocol file.</span>

<code>**class** NullData(Data)</code><br>
<span class="docs">The `NullData` structure. This class does not define any fields.</span>

<code>**class** [StationURL](#stationurl)</code><br>
<span class="docs">A station url (`nn::nex::StationURL`).</span>

<code>**class** [DateTime](#datetime)</code><br>
<span class="docs">A date time object (`nn::nex::DateTime`).</span>

<code>**class** [ResultRange](#resultrange)(Structure)</code><br>
<span class="docs">A result range (`nn::nex::ResultRange`). This structure limits database queries to a specific range.</span>

## RMCError
<code>**def _\_init__**(code: str = "Core::Unknown)</code><br>
<span class="docs">Creates a new RMCError from the given error description.</span>

<code>**def _\_init__**(code: int = 0x10001)</code><br>
<span class="docs">Creates a new RMCError from the given error code.</span>

<code>**def result**() -> [Result](#result)</code><br>
<span class="docs">Returns a result that represents the error.</span>

## Result
<code style="color: blue">@classmethod</code><br>
<code>**def success**(code: str = "Core::Unknown") -> [Result](#result)</code><br>
<span class="docs">Creates a new [`Result`](#result) object that indicates success.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def success**(code: int = 0x10001) -> [Result](#result)</code><br>
<span class="docs">Creates a new [`Result`](#result) object that indicates success.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def error**(code: str = "Core::Unknown") -> [Result](#result)</code><br>
<span class="docs">Creates a new [`Result`](#result) object that indicates an error.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def error**(code: int = 0x10001) -> [Result](#result)</code><br>
<span class="docs">Creates a new [`Result`](#result) object that indicates an error.</span>

<code>**def is_success**() -> bool</code><br>
<span class="docs">Returns `True` if the result indicates success.</span>

<code>**def is_error**() -> bool</code><br>
<span class="docs">Returns `True` if the result indicates an error.</span>

<code>**def code**() -> int</code><br>
<span class="docs">Returns the error code of the result. Errors are indicated by bit `1 << 31`.</span>

<code>**def name**() -> str</code><br>
<span class="docs">Returns a description of the result. If the result indicates success, this method always returns `"success"`, regardless of the error code. If the error bit is set but the error code is unknown, this method returns `"unknown error"`.</span>

<code>**def raise_if_error**() -> None</code><br>
<span class="docs">Raises an `RMCError` if the error bit is set.</span>

## StationURL
A station url consists of an url scheme and a bunch of parameters. The following parameters are currently valid:<br>
<span class="docs">`address`, `Rsa`, `port`, `stream`, `sid`, `PID`, `CID`, `type`, `RVCID`, `natm`, `natf`, `upnp`, `pmp`, `probeinit`, `PRID` and `Rsp`.</span>

<code>**def _\_init__**(scheme: str = "prudp", \**kwargs)</code><br>
<span class="docs">Creates a new station url with the given url scheme. Additional parameters may be provided in `kwargs`.</span>

<code>**def _\_repr__**() -> str</code><br>
<span class="docs">Returns the string representation of the station url.</span>

<code>**def _\_getitem__**(name: str) -> object</code><br>
<span class="docs">Returns a specific parameter, either as `str` or `int`. Returns a default value if the parameter name is valid but not defined in the station url. Raises `KeyError` if the parameter name is invalid.</span>

<code>**def _\_setitem__**(name: str, value: object) -> None</code><br>
<span class="docs">Changes a specific parameter. The given `value` is automatically converted to string.</span>

<code>**def scheme**() -> str</code><br>
<span class="docs">Returns the url scheme.</span>

<code>**def address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address of the station url as a tuple: `(address, port)`.</span>

<code>**def is_public**() -> bool</code><br>
<span class="docs">Returns `True` if the `type` field indicates that the station address is public.</span>

<code>**def is_behind_nat**() -> bool</code><br>
<span class="docs">Returns `True` if the `type` field indicates that the station is behind a nat device.</span>

<code>**def is_global**() -> bool</code><br>
<span class="docs">Returns `True` if the `type` field indicates that the station address is global (i.e. public and not behind a nat device).</span>

<code>**def is_global**() -> [StationURL](#stationurl)</code><br>
<span class="docs">Returns a copy of the station url.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def parse**(string: str) -> [StationURL](#stationurl)</code><br>
<span class="docs">Parses the given station url string. If `string` is empty, the station url is created with the `"prudp"` scheme and without parameters.</span>

## DateTime
A `DateTime` object always represents UTC time.

<code>** def _\_init__**(value: int)</code><br>
<span class="docs">Creates a new [`DateTime`](#datetime) object from the given value.</span>

<code>**def value**() -> int</code><br>
<span class="docs">Returns value of the [`DateTime`](#datetime) object, as encoded by `nex`.</span>

<code>**def second**() -> int</code><br>
<span class="docs">Returns the seconds (0 - 59)</span><br>
<code>**def minute**() -> int</code><br>
<span class="docs">Returns the minutes (0 - 59)</span><br>
<code>**def hour**() -> int</code><br>
<span class="docs">Returns the hours (0 - 23)</span><br>
<code>**def day**() -> int</code><br>
<span class="docs">Returns the day of the month (1 - 31).</span><br>
<code>**def month**() -> int</code><br>
<span class="docs">Returns the month (1 - 12)</span><br>
<code>**def year**() -> int</code><br>
<span class="docs">Returns the year.</span>

<code>**def standard_datetime**() -> datetime.datetime</code><br>
<span class="docs">Converts the [`DateTime`](#datetime) object to a standard `datetime.datetime` object.</span>

<code>**def timestamp**() -> int</code><br>
<span class="docs">Returns a posix timestamp.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def make**(year: int, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0, second: int = 0) -> [DateTime](#datetime)</code><br>
<span class="docs">Creates a new [`DateTime`](#datetime) object for the given date.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def fromtimestamp**(timestamp: int) -> [DateTime](#datetime)</code><br>
<span class="docs">Creates a new [`DateTime`](#datetime) object from the given posix timestamp.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def now**() -> [DateTime](#datetime)</code><br>
<span class="docs">Creates a new [`DateTime`](#datetime) object for the current time.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def never**() -> [DateTime](#datetime)</code><br>
<span class="docs">Creates a special [`DateTime`](#datetime) object that represents 'never'.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def future**() -> [DateTime](#datetime)</code><br>
<span class="docs">Creates a special [`DateTime`](#datetime) object that represents 'future'.</span>

## ResultRange
`offset: int`<br>
`size: int`

<code>**def _\_init__**(offset: int = 0, size: int = 10)</code><br>
<span class="docs">Creates a new result range.</span>
