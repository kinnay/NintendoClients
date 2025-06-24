from nintendo.switch import baas
from anynet import http
import pytest


AUTHENTICATE_REQUEST_1200 = (
	"POST /1.0.0/application/token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 46\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"grantType=public_client&assertion=device.token"
)

AUTHENTICATE_REQUEST_1900 = (
	"POST /1.0.0/application/token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 62\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"grantType=public_client&assertion=device.token&penneId=penneId"
)

AUTHENTICATE_REQUEST_2000 = (
	"POST /1.0.0/application/token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 62\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"grantType=public_client&assertion=device.token&penneId=penneId"
)

LOGIN_REQUEST_1200 = (
	"POST /1.0.0/login HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Authorization: Bearer access.token\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 93\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"id=1234567890abcdef&"
	"password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&"
	"appAuthNToken=app.token"
)

LOGIN_REQUEST_2000 = (
	"POST /1.0.0/login HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)\r\n"
	"Accept: */*\r\n"
	"Authorization: Bearer access.token\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 124\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"id=1234567890abcdef&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&appAuthNToken=app.token&naCountry=NL&isPersistent=true"
)

REGISTER_REQUEST = (
	"POST /1.0.0/users HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Authorization: Bearer access.token\r\n"
	"Content-Length: 0\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"\r\n"
)

UPDATE_PRESENCE_REQUEST_1500 = (
	"PATCH /1.0.0/users/aaaaaaaaaaaaaaaa/device_accounts/bbbbbbbbbbbbbbbb HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/json-patch+json\r\n"
	"Authorization: Bearer access.token\r\n"
	"Content-Length: 315\r\n"
	"\r\n"
	'[{"op":"replace","path":"/presence/state","value":"ONLINE"},'
	'{"op":"add","path":"/presence/extras/friends/appField","value":"{}"},'
	'{"op":"add","path":"/presence/extras/friends/appInfo:appId","value":"010040600c5ce000"},'
	'{"op":"add","path":"/presence/extras/friends/appInfo:presenceGroupId","value":"010040600c5ce000"}]'
)

UPDATE_PRESENCE_REQUEST_1900 = (
	"PATCH /1.0.0/users/aaaaaaaaaaaaaaaa/device_accounts/bbbbbbbbbbbbbbbb HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/json-patch+json\r\n"
	"Authorization: Bearer access.token\r\n"
	"Content-Length: 389\r\n"
	"\r\n"
	'[{"op":"replace","path":"/presence/state","value":"ONLINE"},'
	'{"op":"add","path":"/presence/extras/friends/appField","value":"{}"},'
	'{"op":"add","path":"/presence/extras/friends/appInfo:appId","value":"010040600c5ce000"},'
	'{"op":"add","path":"/presence/extras/friends/appInfo:acdIndex","value":0},'
	'{"op":"add","path":"/presence/extras/friends/appInfo:presenceGroupId","value":"010040600c5ce000"}]'
)

GET_FRIENDS_REQUEST = (
	"GET /2.0.0/users/aaaaaaaaaaaaaaaa/friends?count=300 HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Authorization: Bearer access.token\r\n"
	"\r\n"
)


@pytest.mark.anyio
async def test_authenticate_1200():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_1200
		response = http.HTTPResponse(200)
		response.json = {"accessToken": "access.token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.authenticate("device.token")
		assert response["accessToken"] == "access.token"


@pytest.mark.anyio
async def test_authenticate_1900():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_1900
		response = http.HTTPResponse(200)
		response.json = {"accessToken": "access.token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		response = await client.authenticate("device.token", "penneId")
		assert response["accessToken"] == "access.token"


@pytest.mark.anyio
async def test_authenticate_2000():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_2000
		response = http.HTTPResponse(200)
		response.json = {"accessToken": "access.token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.authenticate("device.token", "penneId")
		assert response["accessToken"] == "access.token"


@pytest.mark.anyio
async def test_login_1200():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_1200
		response = http.HTTPResponse(200)
		response.json = {"idToken": "id.token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.login(
			0x1234567890ABCDEF, "a" * 40, "access.token", "app.token"
		)
		assert response["idToken"] == "id.token"


@pytest.mark.anyio
async def test_login_2000():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_2000
		response = http.HTTPResponse(200)
		response.json = {"idToken": "id.token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.login(
			0x1234567890ABCDEF, "a" * 40, "access.token", "app.token", "NL"
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
		client.set_system_version(1500)
		client.set_context(None)
		await client.register("access.token")


@pytest.mark.anyio
async def test_update_presence_1500():
	async def handler(client, request):
		assert request.encode().decode() == UPDATE_PRESENCE_REQUEST_1500
		return http.HTTPResponse(200)

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		await client.update_presence(
			0xAAAAAAAAAAAAAAAA,
			0xBBBBBBBBBBBBBBBB,
			"access.token",
			baas.PresenceState.ONLINE,
			0x010040600C5CE000,
			0x010040600C5CE000,
		)


@pytest.mark.anyio
async def test_update_presence_1900():
	async def handler(client, request):
		assert request.encode().decode() == UPDATE_PRESENCE_REQUEST_1900
		return http.HTTPResponse(200)

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		await client.update_presence(
			0xAAAAAAAAAAAAAAAA,
			0xBBBBBBBBBBBBBBBB,
			"access.token",
			baas.PresenceState.ONLINE,
			0x010040600C5CE000,
			0x010040600C5CE000,
		)


@pytest.mark.anyio
async def test_get_friends():
	async def handler(client, request):
		assert request.encode().decode() == GET_FRIENDS_REQUEST
		return http.HTTPResponse(200)

	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		await client.get_friends(0xAAAAAAAAAAAAAAAA, "access.token")
