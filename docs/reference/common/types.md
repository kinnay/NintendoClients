
# Module: <code>nintendo.common.types</code>

Provides a case insensitive dictionary type.

<code>**class** [MappedDict](#mappeddict)</code><br>
<span class="docs">Base class for dicts with internal key transformation.</span>

<code>**class** CaseInsensitiveDict([MappedDict](#mappeddict))</code>
<span class="docs">A dictionary with case insensitive keys. Raises `TypeError` if an item is inserted with a key that is not a string.</span>

## MappedDict
This class provides the same methods as a regular `dict`, except that it transforms the keys internally. The original keys are preserved. For example, [`MappedDict`](#mappeddict)`.keys()` returns the original keys. If multiple keys map to the same internal key only the last original key is stored.

<code>**def standard_dict**() -> dict</code><br>
<span class="docs">Converts the [`MappedDict`](#mappeddict) to a standard Python `dict` with the original keys.</span>

<code>**def mapped_dict**() -> dict</code><br>
<span class="docs">Converts the [`MappedDict`](#mappeddict) to a standard Python `dict` with the transformed keys.</span>

<code>**def transform_key**(key: object) -> object</code><br>
<span class="docs">Transforms the key. This method should be overridden by subclasses.</span>
