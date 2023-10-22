
from nintendo.switch import baas
from anynet import http
import pytest
import struct


AUTHENTICATE_REQUEST = \
	"POST /1.0.0/application/token HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 46\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"grantType=public_client&assertion=device.token"

LOGIN_REQUEST = \
	"POST /1.0.0/login HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Authorization: Bearer access.token\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 93\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"id=1234567890abcdef&" \
	"password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&" \
	"appAuthNToken=app.token"

REGISTER_REQUEST = \
	"POST /1.0.0/users HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Authorization: Bearer access.token\r\n" \
	"Content-Length: 0\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"\r\n"

UPDATE_PRESENCE_REQUEST = \
	"PATCH /1.0.0/users/aaaaaaaaaaaaaaaa/device_accounts/bbbbbbbbbbbbbbbb HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Content-Type: application/json-patch+json\r\n" \
	"Authorization: Bearer access.token\r\n" \
	"Content-Length: 315\r\n" \
	"\r\n" \
	'[{"op":"replace","path":"/presence/state","value":"ONLINE"},' \
	'{"op":"add","path":"/presence/extras/friends/appField","value":"{}"},' \
	'{"op":"add","path":"/presence/extras/friends/appInfo:appId","value":"010040600c5ce000"},' \
	'{"op":"add","path":"/presence/extras/friends/appInfo:presenceGroupId","value":"010040600c5ce000"}]'

GET_FRIENDS_REQUEST = \
	"GET /2.0.0/users/aaaaaaaaaaaaaaaa/friends?count=300 HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Authorization: Bearer access.token\r\n" \
	"\r\n"
	

@pytest.mark.anyio
async def test_authentication():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST
		response = http.HTTPResponse(200)
		response.json = {
			"accessToken": "access.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.authenticate("device.token")
		assert response["accessToken"] == "access.token"

@pytest.mark.anyio
async def test_login():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST
		response = http.HTTPResponse(200)
		response.json = {
			"idToken": "id.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.login(
			0x1234567890abcdef, "a" * 40, "access.token", "app.token"
		)
		assert response["idToken"] == "id.token"

@pytest.mark.anyio
async def test_register():
	async def handler(client, request):
		assert request.encode().decode() == REGISTER_REQUEST
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1501)
		client.set_context(None)
		await client.register("access.token")

@pytest.mark.anyio
async def test_update_presence():
	async def handler(client, request):
		assert request.encode().decode() == UPDATE_PRESENCE_REQUEST
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1501)
		client.set_context(None)
		await client.update_presence(
			0xaaaaaaaaaaaaaaaa, 0xbbbbbbbbbbbbbbbb, "access.token",
			baas.PresenceState.ONLINE, 0x010040600c5ce000, 0x010040600c5ce000
		)

@pytest.mark.anyio
async def test_get_friends():
	async def handler(client, request):
		assert request.encode().decode() == GET_FRIENDS_REQUEST
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1501)
		client.set_context(None)
		await client.get_friends(0xaaaaaaaaaaaaaaaa, "access.token")
