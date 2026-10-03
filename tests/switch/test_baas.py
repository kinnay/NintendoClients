
from nintendo.switch import baas
from anynet import http
import pytest


AUTHENTICATE_REQUEST_1200 = \
"""POST /1.0.0/application/token HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)
Accept: */*
X-Nintendo-PowerState: FA
Content-Length: 46
Content-Type: application/x-www-form-urlencoded

grantType=public_client&assertion=device.token"""

AUTHENTICATE_REQUEST_1900 = \
"""POST /1.0.0/application/token HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)
Accept: */*
X-Nintendo-PowerState: FA
Content-Length: 62
Content-Type: application/x-www-form-urlencoded

grantType=public_client&assertion=device.token&penneId=penneId"""

AUTHENTICATE_REQUEST_2000 = \
"""POST /1.0.0/application/token HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)
Accept: */*
X-Nintendo-PowerState: FA
Content-Length: 62
Content-Type: application/x-www-form-urlencoded

grantType=public_client&assertion=device.token&penneId=penneId"""

AUTHENTICATE_REQUEST_2301 = \
"""POST /1.0.0/application/token HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 23.3.0.0; Add-on 23.3.0.0)
Content-Type: application/x-www-form-urlencoded
X-Nintendo-PowerState: FA
Content-Length: 62

grantType=public_client&assertion=device.token&penneId=penneId"""

LOGIN_REQUEST_1200 = \
"""POST /1.0.0/login HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)
Accept: */*
Authorization: Bearer access.token
X-Nintendo-PowerState: FA
Content-Length: 93
Content-Type: application/x-www-form-urlencoded

id=1234567890abcdef&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&appAuthNToken=app.token"""

LOGIN_REQUEST_2000 = \
"""POST /1.0.0/login HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)
Accept: */*
Authorization: Bearer access.token
X-Nintendo-PowerState: FA
Content-Length: 124
Content-Type: application/x-www-form-urlencoded

id=1234567890abcdef&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&appAuthNToken=app.token&naCountry=NL&isPersistent=true"""

LOGIN_REQUEST_2110 = \
"""POST /1.0.0/login HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer access.token
X-Nintendo-PowerState: FA
Content-Length: 124

id=1234567890abcdef&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&appAuthNToken=app.token&naCountry=NL&isPersistent=true"""

LOGIN_REQUEST_2301 = \
"""POST /1.0.0/login HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 23.3.0.0; Add-on 23.3.0.0)
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer access.token
X-Nintendo-PowerState: FA
Content-Length: 124

id=1234567890abcdef&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&appAuthNToken=app.token&naCountry=NL&isPersistent=true"""

REGISTER_REQUEST = \
"""POST /1.0.0/users HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access.token
Content-Length: 0
Content-Type: application/x-www-form-urlencoded

"""

UPDATE_PRESENCE_REQUEST_1500 = \
"""PATCH /1.0.0/users/aaaaaaaaaaaaaaaa/device_accounts/bbbbbbbbbbbbbbbb HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Content-Type: application/json-patch+json
Authorization: Bearer access.token
Content-Length: 315

[{"op":"replace","path":"/presence/state","value":"ONLINE"},{"op":"add","path":"/presence/extras/friends/appField","value":"{}"},{"op":"add","path":"/presence/extras/friends/appInfo:appId","value":"010040600c5ce000"},{"op":"add","path":"/presence/extras/friends/appInfo:presenceGroupId","value":"010040600c5ce000"}]"""

UPDATE_PRESENCE_REQUEST_1900 = \
"""PATCH /1.0.0/users/aaaaaaaaaaaaaaaa/device_accounts/bbbbbbbbbbbbbbbb HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)
Accept: */*
Content-Type: application/json-patch+json
Authorization: Bearer access.token
Content-Length: 389

[{"op":"replace","path":"/presence/state","value":"ONLINE"},{"op":"add","path":"/presence/extras/friends/appField","value":"{}"},{"op":"add","path":"/presence/extras/friends/appInfo:appId","value":"010040600c5ce000"},{"op":"add","path":"/presence/extras/friends/appInfo:acdIndex","value":0},{"op":"add","path":"/presence/extras/friends/appInfo:presenceGroupId","value":"010040600c5ce000"}]"""

GET_FRIENDS_REQUEST = \
"""GET /2.0.0/users/aaaaaaaaaaaaaaaa/friends?count=300 HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access.token

"""
	

@pytest.mark.anyio
async def test_authenticate_1200():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_1200.replace("\n", "\r\n")
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
async def test_authenticate_1900():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_1900.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"accessToken": "access.token"
		}
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
		assert request.encode().decode() == AUTHENTICATE_REQUEST_2000.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"accessToken": "access.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.authenticate("device.token", "penneId")
		assert response["accessToken"] == "access.token"

@pytest.mark.anyio
async def test_authenticate_2301():
	async def handler(client, request):
		assert request.encode().decode() == AUTHENTICATE_REQUEST_2301.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"accessToken": "access.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2301)
		client.set_context(None)
		response = await client.authenticate("device.token", "penneId")
		assert response["accessToken"] == "access.token"

@pytest.mark.anyio
async def test_login_1200():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_1200.replace("\n", "\r\n")
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
async def test_login_2000():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_2000.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"idToken": "id.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.login(
			0x1234567890abcdef, "a" * 40, "access.token", "app.token", "NL"
		)
		assert response["idToken"] == "id.token"

@pytest.mark.anyio
async def test_login_2110():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_2110.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"idToken": "id.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2110)
		client.set_context(None)
		response = await client.login(
			0x1234567890abcdef, "a" * 40, "access.token", "app.token", "NL"
		)
		assert response["idToken"] == "id.token"

@pytest.mark.anyio
async def test_login_2301():
	async def handler(client, request):
		assert request.encode().decode() == LOGIN_REQUEST_2301.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"idToken": "id.token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(2301)
		client.set_context(None)
		response = await client.login(
			0x1234567890abcdef, "a" * 40, "access.token", "app.token", "NL"
		)
		assert response["idToken"] == "id.token"

@pytest.mark.anyio
async def test_register():
	async def handler(client, request):
		assert request.encode().decode() == REGISTER_REQUEST.replace("\n", "\r\n")
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
		assert request.encode().decode() == UPDATE_PRESENCE_REQUEST_1500.replace("\n", "\r\n")
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		await client.update_presence(
			0xaaaaaaaaaaaaaaaa, 0xbbbbbbbbbbbbbbbb, "access.token",
			baas.PresenceState.ONLINE, 0x010040600c5ce000, 0x010040600c5ce000
		)

@pytest.mark.anyio
async def test_update_presence_1900():
	async def handler(client, request):
		assert request.encode().decode() == UPDATE_PRESENCE_REQUEST_1900.replace("\n", "\r\n")
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		await client.update_presence(
			0xaaaaaaaaaaaaaaaa, 0xbbbbbbbbbbbbbbbb, "access.token",
			baas.PresenceState.ONLINE, 0x010040600c5ce000, 0x010040600c5ce000
		)

@pytest.mark.anyio
async def test_get_friends():
	async def handler(client, request):
		assert request.encode().decode() == GET_FRIENDS_REQUEST.replace("\n", "\r\n")
		return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		client = baas.BAASClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		await client.get_friends(0xaaaaaaaaaaaaaaaa, "access.token")
