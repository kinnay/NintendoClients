
from nintendo.common import types
import pytest


TEST = {
	"Hi": "hello",
	"Test": "TEST"
}


class TestCaseInsensitiveDict:
	def test_init_empty(self):
		test = types.CaseInsensitiveDict()
		assert test == {}
		
	def test_init_dict(self):
		test = types.CaseInsensitiveDict(TEST, HI = "hey")
		assert test == {"hI": "hey", "test": "TEST"}
		
	def test_init_items(self):
		test = types.CaseInsensitiveDict([("Hi", "hello"), ("Test", "TEST")], HI = "hey")
		assert test == {"hI": "hey", "test": "TEST"}
		
	def test_standard_dict(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test.standard_dict() == TEST
		
	def test_fromkeys(self):
		test = types.CaseInsensitiveDict.fromkeys(["a", "B"], 123)
		assert test == {"a": 123, "b": 123}
	
	def test_iter(self):
		test = types.CaseInsensitiveDict(TEST)
		for i, item in enumerate(test):
			assert item == ["Hi", "Test"][i]
	
	def test_len(self):
		test = types.CaseInsensitiveDict(TEST)
		assert len(test) == 2
		
	def test_bool(self):
		test = types.CaseInsensitiveDict()
		assert not test
	
		test = types.CaseInsensitiveDict(TEST)
		assert test
	
	def test_contains(self):
		test = types.CaseInsensitiveDict(TEST)
		assert "Hi" in test
		assert "tEsT" in test
		assert "hello" not in test
	
	def test_getitem(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test["HI"] == "hello"
		
		with pytest.raises(KeyError):
			test["hello"]
		with pytest.raises(TypeError):
			test[b"HI"]
	
	def test_setitem(self):
		test = types.CaseInsensitiveDict(TEST)
		test["hi"] = "hello!"
		test["hey"] = "hi"
		assert test == {"hi": "hello!", "hey": "hi", "test": "TEST"}
		
		with pytest.raises(TypeError):
			test[0] = "hi"
		with pytest.raises(TypeError):
			test[b"hi"] = "hi"
	
	def test_delitem(self):
		test = types.CaseInsensitiveDict(TEST)
		del test["hI"]
		assert test == {"test": "TEST"}
		
	def test_clear(self):
		test = types.CaseInsensitiveDict(TEST)
		test.clear()
		assert test == {}
		
	def test_copy(self):
		test = types.CaseInsensitiveDict(TEST)
		copy = test.copy()
		assert test == copy
		
		copy["hi"] = "hello!"
		assert test != copy
		
	def test_get(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test.get("hi") == "hello"
		assert test.get("hi", 1) == "hello"
		assert test.get("hey") is None
		assert test.get("hey", 1) == 1
	
	def test_pop(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test.pop("hI") == "hello"
		assert "hI" not in test
		
		with pytest.raises(KeyError):
			test.pop("hI")
		
		assert test.pop("hI", None) is None
		assert test.pop("hI", 1) == 1
		
	def test_popitem(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test.popitem() == ("Test", "TEST")
		assert test == {"hi": "hello"}
		
	def test_setdefault(self):
		test = types.CaseInsensitiveDict(TEST)
		assert test.setdefault("hi", "hey") == "hello"
		assert test == TEST
		
		assert test.setdefault("hey", "hi") == "hi"
		assert test == {"hi": "hello", "test": "TEST", "hey": "hi"}
		
		assert test.setdefault("hey") == "hi"
		assert test == {"hi": "hello", "test": "TEST", "hey": "hi"}
		
		assert test.setdefault("hello") is None
		assert test == {"hi": "hello", "test": "TEST", "hey": "hi", "hello": None}
		
	def test_keys(self):
		test = types.CaseInsensitiveDict(TEST)
		assert list(test.keys()) == ["Hi", "Test"]
	
	def test_values(self):
		test = types.CaseInsensitiveDict(TEST)
		assert list(test.values()) == ["hello", "TEST"]
	
	def test_items(self):
		test = types.CaseInsensitiveDict(TEST)
		assert list(test.items()) == [("Hi", "hello"), ("Test", "TEST")]
	
	def test_update_empty(self):
		test = types.CaseInsensitiveDict(TEST)
		test.update()
		assert test == TEST
		
	def test_update_dict(self):
		test = types.CaseInsensitiveDict(TEST)
		test.update({"hi": "hey", "hey": "hi"})
		assert test == {"hi": "hey", "hey": "hi", "test": "TEST"}
		
	def test_update_items(self):
		test = types.CaseInsensitiveDict(TEST)
		test.update([("hi", "hey"), ("hey", "hi")], HEY="hello")
		assert test == {"hi": "hey", "hey": "hello", "test": "TEST"}
