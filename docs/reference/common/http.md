
# Module: <code>nintendo.common.http</code>

Provides HTTP-related classes, including a client and a server. Only basic HTTP features are supported.

<code>**class** HTTPError(Exception)</code><br>
<span class="docs">General exception for errors related to HTTP.</span>

<code>**class** [HTTPMessage](#httpmessage)</code><br>
<span class="docs">Base class for HTTP messages. This class should not be instantiated directly. Instead, one of its subclasses should be used.

<code>**class** [HTTPRequest](#httprequest)([HTTPMessage](#httpmessage))</code><br>
<span class="docs">A HTTP request object.</span>

<code>**class** [HTTPResponse](#httpresponse)([HTTPMessage](#httpmessage))</code><br>
<span class="docs">A HTTP response object.</span>

<code>**async def get**(url: string, *, headers: dict[str, str] = {}, context: [TLSContext](../tls#tlscontext) = None) -> [HTTPResponse](#httpresponse)</code><br>
<span class="docs">Performs a GET request. If `context` is provided, the connection is secured with TLS.</span>

<code>**async def request**(req: [HTTPRequest](#httprequest), context: [TLSContext](../tls#tlscontext) = None) -> [HTTPResponse](#httpresponse)</code><br>
<span class="docs">Performs an HTTP request. The server address is derived from the `Host` header of the HTTP request. If `context` is provided, the connection is secured with TLS. Raises `HTTPError` if the response could not be parsed.</span>

<code>**async with serve**(handler: Callable, host: str = "", port: int = 0, context: [TLSContext](#tlscontext) = None) -> None</code><br>
<span class="docs">Creates an HTTP server at the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system. If `context` is provided, the server is secured with TLS.<br><br>
`handler` should be an `async` function that takes an [`HTTPRequest`](#httprequest) and returns an [`HTTPResponse`](#httpresponse). It's possible to call blocking functions in `handler`, because the HTTP server spawns a new task for each request. If `handler` raises an exception the server sends an empty HTTP response with status code `500` to the client.</span>

<code>**def urlencode**(data: str) -> str</code><br>
<span class="docs">Applies url-encoding on the given string (i.e. replaces special characters by `%XX`).</span>

<code>**def urldecode**(data: str) -> str</code><br>
<span class="docs">Decodes the given url-encoded string.</span>

<code>**def formencode**(data: dict[str, str], url: bool = True) -> str</code><br>
<span class="docs">Encodes `data` using form-encoding. If `url` is `True`, field names and values are url-encoded automatically.</span>

<code>**def formdecode**(data: str, url: bool = True) -> dict[str, str]</code><br>
<span class="docs">Parses a form-encoded string. If `url` is `True`, field names and values are automatically url-decoded. Raises `HTTPError` if the given string is not form-encoded correctly.</span>

## HTTPMessage
This is the base class of [`HTTPRequest`](#httprequest) and [`HTTPResponse`](#httpresponse). This class should not be instantiated directly. Instead, one of its subclasses should be used.

This class provides several attributes that define the body of the HTTP message. In general, only one of them should be used. When the HTTP message is encoded, the attributes are evaluated in the following order: `plainform`, `form`, `json`, `xml`, `files`, `text` and `body`. The first non-empty attribute defines the body of the HTTP request. The others are ignored.

Most headers are left unchanged when the HTTP message is encoded. However, if no `Content-Type` header is present, a default is chosen based on the attribute that defines the body, unless the body is empty. The `Content-Length` header is always overwritten, unless the `Transfer-Encoding` is `chunked` or the body is empty.

When a HTTP message is parsed, the `body` attribute is always filled in. The other attributes are only filled if they fit the `Content-Type` of the HTTP message.

<code>**version**: str = "HTTP/1.1"</code><br>
<span class="docs">The version of the HTTP message. Only `HTTP/1.1` is supported.</span>

<code>**headers**: [CaseInsensitiveDict](../types)[str, str] = {}</code><br>
<span class="docs">The HTTP headers. Be careful with overwriting this attribute. If you accidentally overwrite it with a regular `dict` it loses its case insensitivity.

<code>**body**: bytes = ""</code><br>
<span class="docs">The raw body of the HTTP message. The `Content-Type` defaults to `application/octet-stream`.</span>

<code>**text**: str = None</code><br>
<span class="docs">The decoded body of the HTTP message, if applicable. The `Content-Type` defaults to `text/plain`.</span>

<code>**files**: dict[str, bytes] = {}</code><br>
<span class="docs">A list of binary files. The `Content-Type` defaults to `multipart/form-data`.

<code>**boundary**: str = "--------BOUNDARY--------"</code><br>
<span class="docs">The boundary string that's used if the body is encoded from `files`.</span>

<code>**form**: dict[str, str] = {}</code><br>
<span class="docs">The form parameters in the body. The parameters are url-encoded automatically. The `Content-Type` defaults to `application/x-www-form-urlencoded`.

<code>**plainform**: dict[str, str] = {}</code><br>
<span class="docs">The form parameters in the body. The difference with the `form` attribute is that the names and values are *not* url-encoded automatically. The `Content-Type` defaults to `application/x-www-form-urlencoded`.

<code>**json**: dict = {}</code><br>
<span class="docs">The JSON body. The `Content-Type` defaults to `application/json`.

<code>**xml**: [XMLTree](../xml#xmltree) = None</code><br>
<span class="docs">An [XMLTree](../xml#xmltree) that represents the body. The `Content-Type` defaults to `application/xml`.

<code>**def encode**() -> bytes</code><br>
<span class="docs">Encodes the HTTP message.</span>

<code>**def encode_headers**() -> bytes</code><br>
<span class="docs">Encodes only the headers of the HTTP message.</span>

<code>**def encode_body**() -> bytes</code><br>
<span class="docs">Encodes only the body of the HTTP message.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def parse**(data: bytes) -> [`HTTPMessage`](#httpmessage)</code><br>
<span class="docs">Parses a HTTP message. This method should not be called on the [`HTTPMessage`](#httpmessage) class. Instead, it should be called on one of its subclasses. This method always fills in the `body` attribute. The other attributes that define the body (such as `text` or `json`) are only set if they fit the `Content-Type` of the HTTP message. Raises `HTTPError` if the given data does not contain a valid HTTP message.

## HTTPRequest
This class inherits [`HTTPMessage`](#httpmessage). During encoding, the `Expect` header is set to `100-continue` if the size of the body exceeds a given threshold.

<code>**method**: str = "GET"</code><br>
<span class="docs">The HTTP method.</span>

<code>**path**: str = "/"</code><br>
<span class="docs">The path of the HTTP request.</span>

<code>**params**: dict[str, str] = {}</code><br>
<span class="docs">The GET parameters behind the `path`. The parameters are url-encoded automatically.</span>

<code>**continue_threshold**: int = 1024</code><br>
<span class="docs">The size of the body after which the `Expect` header is set to `100-continue`. If set to `None`, the `Expect` header is never modified, regardless of the body size.

<code>**certificate**: [`TLSCertificate`](../tls#tlscertificate) = None</code><br>
<span class="docs">The client certificate of the request. If `None`, no client certificate is used. This attribute is only relevant on servers. For HTTP clients, the certificate must be specified in the [`TLSContext`](../tls#tlscontext) that is passed to `request`.</span>

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new HTTP request.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def get**(path: str) -> [HTTPRequest](#httprequest)</code><br>
<span class="docs">Convenience method that creates a GET request with the given path.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def post**(path: str) -> [HTTPRequest](#httprequest)</code><br>
<span class="docs">Convenience method that creates a POST request with the given path.</span>

## HTTPResponse
This class inherits [`HTTPMessage`](#httpmessage).

<code>**status_code**: int = 500</code><br>
<span class="docs">The status code of the HTTP response.</span>

<code>**status_name**: str = "Internal Server Error"</code><br>
<span class="docs">The reason string of the HTTP response.</span>

<code>**def _\_init__**(status_code: int = 500)</code><br>
<span class="docs">Creates a new HTTP response with the given status code. `status_name` is derived from the given status code. If the given status code is not recognized, `status_name` is set to `"Unknown"`</span>

<code>**def success**() -> bool</code><br>
<span class="docs">Returns `True` if the status code indicates success, i.e. if it has the form `2xx`.

<code>**def error**() -> bool</code><br>
<span class="docs">This is the reverse of `success`. Returns `True` if the status code does not indicate success.

<code>**def raise_if_error**() -> None</code><br>
<span class="docs">Raises `HTTPError` if the status code does not indicate success.</span>
