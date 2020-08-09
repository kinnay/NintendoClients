
from nintendo.common import http, xml, tls
import pytest


NAME = "localhost"
HOST = "127.0.0.1"


def test_formdecode():
	assert http.formdecode("") == {}
	assert http.formdecode("a=b&b=a") == {
		"a": "b", "b": "a"
	}
	assert http.formdecode(
		"123%20456=%26%3d%3F&-_=-_&~="
	) == {"123 456": "&=?", "-_": "-_", "~": ""}
	assert http.formdecode(
		"123%20456=%26%3d%3F&-_=-_&~=", False
	) == {"123%20456": "%26%3d%3F", "-_": "-_", "~": ""}
	
	with pytest.raises(http.HTTPError):
		http.formdecode("&&&")

def test_formencode():
	assert http.formencode({}) == ""
	assert http.formencode({"a": "b", "b": "a"}) == "a=b&b=a"
	assert http.formencode({
		"123 456": "&=?", "-_": "-_", "~": ""
	}) == "123%20456=%26%3D%3F&-_=-_&~="
	assert http.formencode({
		"123 456": "&=?", "-_": "-_", "~": ""
	}, False) == "123 456=&=?&-_=-_&~="


class TestHTTP:	@pytest.mark.anyio
	async def test_ok(self):
		async def handler(request):
			assert request.method == "GET"
			assert request.path == "/test/ok"
			response = http.HTTPResponse(200)
			return response
	
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest.get("/test/ok")
			request.headers["Host"] = "%s:12345" %HOST
			response = await http.request(request)
			assert response.status_code == 200
			assert response.status_name == "OK"
			assert response.success()
		@pytest.mark.anyio
	async def test_error(self):
		async def handler(request):
			assert request.method == "POST"
			assert request.path == "/test/error"
			status = int(request.headers["X-Status-Code"])
			response = http.HTTPResponse(status)
			return response
		
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest.post("/test/error")
			request.headers["Host"] = "%s:12345" %HOST
			request.headers["X-Status-Code"] = 404
			response = await http.request(request)
			assert response.status_code == 404
			assert response.status_name == "Not Found"
			assert response.error()
			
			request = http.HTTPRequest.post("/test/error")
			request.headers["Host"] = "%s:12345" %HOST
			request.headers["X-Status-Code"] = 678
			response = await http.request(request)
			assert response.status_code == 678
			assert response.status_name == "Unknown"
			@pytest.mark.anyio
	async def test_exception(self):
		async def handler(request):
			raise ValueError("Oops")
	
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			response = await http.request(request)
			assert response.status_code == 500
			assert response.status_name == "Internal Server Error"
	
	@pytest.mark.anyio
	async def test_get(self):
		async def handler(request):
			assert request.path == "/test/get"
			return http.HTTPResponse(200)
		
		async with http.serve(handler, HOST, 12345):
			response = await http.get("%s:12345/test/get" %HOST)
			assert response.success()
		@pytest.mark.anyio
	async def test_body(self):
		async def handler(request):
			assert request.body == b"abcdef"
			response = http.HTTPResponse(200)
			response.headers["X-Content-Size"] = len(request.body)
			return response
	
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.body = b"abcdef"
			response = await http.request(request)
			assert response.headers["X-Content-Size"] == "6"
			@pytest.mark.anyio
	async def test_text(self):
		async def handler(request):
			assert request.body == b"Hello"
			response = http.HTTPResponse(200)
			response.text = request.text.upper()
			return response
		
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.text = "Hello"
			response = await http.request(request)
			assert response.text == "HELLO"
		@pytest.mark.anyio
	async def test_continue(self):
		async def handler(request):
			response = http.HTTPResponse(200)
			response.body = request.body
			return response
	
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.continue_threshold = 64
			request.body = b"a" * 80
			response = await http.request(request)
			assert response.body == b"a" * 80
		@pytest.mark.anyio
	async def test_plainform(self):
		async def handler(request):
			assert request.text == "+value +=!=?"
			response = http.HTTPResponse(200)
			response.plainform = {
				"$<result>": request.plainform["+value +"]
			}
			return response
		
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.plainform = {
				"+value +": "!=?"
			}
			response = await http.request(request)
			assert response.plainform["$<result>"] == "!=?"
	@pytest.mark.anyio
	async def test_form(self):
		async def handler(request):
			response = http.HTTPResponse(200)
			response.form = {
				"$<result>": request.form["&value"]
			}
			return response
		
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.form = {
				"&value": "&=?"
			}
			response = await http.request(request)
			assert response.form["$<result>"] == "&=?"
			
	@pytest.mark.anyio
	async def test_json(self):
		async def handler(request):
			response = http.HTTPResponse(200)
			response.json = {
				"result": request.json["value"]
			}
			return response
		
		async with http.serve(handler, HOST, 12345):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.json = {
				"value": True
			}
			response = await http.request(request)
			assert response.json["result"] is True
			
	@pytest.mark.anyio
	async def test_xml(self):
		async def handler(request):
			assert request.xml.name == "value"
			tree = xml.XMLTree("result")
			tree.text = request.xml.text
			response = http.HTTPResponse(200)
			response.xml = tree
			return response
		
		async with http.serve(handler, HOST, 12345):
			tree = xml.XMLTree("value")
			tree.text = "12345"
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %HOST
			request.xml = tree
			response = await http.request(request)
			assert response.xml.name == "result"
			assert response.xml.text == "12345"
			
	@pytest.mark.anyio
	async def test_certificate(self):
		# Create a self signed server certificate
		serverkey = tls.TLSPrivateKey.generate()
		servercert = tls.TLSCertificate.generate(serverkey)
		servercert.subject["CN"] = NAME
		servercert.issuer["CN"] = NAME
		servercert.sign(serverkey)
		
		# Create a certificate authority for the client certificate
		authoritykey = tls.TLSPrivateKey.generate()
		authoritycert = tls.TLSCertificate.generate(authoritykey)
		authoritycert.subject["CN"] = "authority"
		authoritycert.issuer["CN"] = "authority"
		authoritycert.sign(authoritykey)
		
		# Create a client certificate and sign it
		clientkey = tls.TLSPrivateKey.generate()
		clientcert = tls.TLSCertificate.generate(clientkey)
		clientcert.subject["CN"] = "testclient"
		clientcert.issuer["CN"] = "authority"
		clientcert.sign(authoritykey)
		
		# Create TLS context for the server
		servercontext = tls.TLSContext()
		servercontext.set_certificate(servercert, serverkey)
		servercontext.set_authority(authoritycert)
		
		clientcontext = tls.TLSContext()
		clientcontext.set_certificate(clientcert, clientkey)
		clientcontext.set_authority(servercert)
		
		async def handler(request):
			assert request.certificate.subject["CN"] == "testclient"
			return http.HTTPResponse(200)
		
		async with http.serve(handler, HOST, 12345, servercontext):
			request = http.HTTPRequest()
			request.headers["Host"] = "%s:12345" %NAME
			response = await http.request(request, clientcontext)
			assert response.success()
