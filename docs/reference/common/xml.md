
# Module: <code>nintendo.common.xml</code>

Provides classes and functions to work with XML documents.

<code>**class** [XMLTree](#xmltree)</code><br>
<span class="docs">Represents an XML tree or a subtree.</span>

<code>**def parse**(text: str) -> [XMLTree](#xmltree)</code><br>
<span class="docs">Parses an XML document and returns an [XMLTree](#xmltree). Entities are decoded automatically. Raises `ValueError` is `text` does not contain a valid XML document.</span>

## XMLTree
<code>**children**: list[[XMLTree](#xmltree)] = []</code><br>
<span class="docs">The children of the root node.

<code>**attrs**: dict[str, str] = {}</code><br>
<span class="docs">The attributes of the root node.</span>

<code>**text**: str = ""</code><br>
<span class="docs">The text in the root node that does not belong to a child tag.</span>

<code>**name**: str = ""</code><br>
<span class="docs">The tag name of the root node</span>

<code>**def _\_init__**(name: str)</code><br>
<span class="docs">Creates a new XML tree with the given tag name.</span>

<code>**def _\_contains__**(name: str) -> bool</code><br>
<span class="docs">Checks if a child with the given tag name exists.</span>

<code>**def _\_getitem__**(name: str) -> [XMLTree](#xmltree)</code><br>
<span class="docs">Returns the first child with the given tag name. Raises `KeyError` if no such child exists.</span>

<code>**def _\_iter__**() -> Iterator</code><br>
<span class="docs">Returns an iterator over the children.</span>

<code>**def _\_len__**() -> int</code><br>
<span class="docs">Returns the number of children.</span>

<code>**def find**(name: str) -> list[[XMLTree](#xmltree)]</code><br>
<span class="docs">Returns all children with the given tag name.</span>

<code>**def add**(name: str, text: str = "", attrs: dict[str, str] = {}) -> [XMLTree](#xmltree)</code><br>
<span class="docs">Creates a new child with the given tag name, text and attributes, and adds it to the XML tree. Returns the new child.

<code>**def encode**() -> str</code><br>
<span class="docs">Encodes the XML tree recursively. Special characters are converted to entities automatically. No insignificant whitespace or XML declaration is added to the document.</span>
