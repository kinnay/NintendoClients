
from nintendo.common import xml
import pytest


DOCUMENT = "<root><key>hi</key><value>test</value></root>"


class TestXMLTree:
	def test_encode(self):
		tree = xml.XMLTree("root")
		assert tree.encode() == "<root></root>"
	
	def test_parse(self):
		tree = xml.parse(DOCUMENT)
		assert tree.encode() == DOCUMENT
	
	def test_attrs(self):
		tree = xml.parse(DOCUMENT)
		assert tree.children[0].name == "key"
		assert tree.children[0].text == "hi"
		assert tree.children[1].name == "value"
		assert tree.children[1].text == "test"
		assert tree.attrs == {}
		assert tree.text == ""
		assert tree.name == "root"
	
	def test_add(self):
		tree = xml.XMLTree("root")
		child1 = tree.add("p", "hi")
		child2 = tree.add("p", "hello", {"attr": "42"})
		assert child1.encode() == "<p>hi</p>"
		assert child2.encode() == "<p attr=\"42\">hello</p>"
		assert tree.encode() == "<root>%s%s</root>" %(child1.encode(), child2.encode())
		
	def test_contains(self):
		tree = xml.parse(DOCUMENT)
		assert "key" in tree
		assert not "root" in tree
		
	def test_getitem(self):
		tree = xml.parse(DOCUMENT)
		assert tree["key"] == tree.children[0]
		with pytest.raises(KeyError):
			tree["root"]
			
	def test_iter(self):
		tree = xml.parse(DOCUMENT)
		assert list(tree) == tree.children
	
	def test_find(self):
		tree = xml.parse(DOCUMENT)
		assert tree.find("key") == [tree.children[0]]
		assert tree.find("root") == []
