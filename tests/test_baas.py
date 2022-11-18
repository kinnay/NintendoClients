
from nintendo import baas
from anynet import http
import pytest
import struct


ACCESS_REQUEST = \
	"POST /1.0.0/application/token HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 46\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"grantType=public_client&assertion=device.token"

LOGIN_REQUEST = \
	"POST /1.0.0/login HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Authorization: Bearer access.token\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 93\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"id=1234567890abcdef&" \
	"password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&" \
	"appAuthNToken=app.token"


@pytest.mark.anyio
async def test_baas():
	async def handler(client, request):
		if request.path == "/1.0.0/application/token":
			assert request.encode().decode() == ACCESS_REQUEST
			response = http.HTTPResponse(200)
			response.json = {
				"accessToken": "access.token"
			}
			return response
		else:
			assert request.encode().decode() == LOGIN_REQUEST
			response = http.HTTPResponse(200)
			response.json = {
				"idToken": "id token"
			}
			return response
			
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = baas.BAASClient()
		client.set_host("127.0.0.1:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.authenticate("device.token")
		token = response["accessToken"]
		response = await client.login(
			0x1234567890abcdef, "a" * 40, token, "app.token"
		)
		assert response["idToken"] == "id token"
