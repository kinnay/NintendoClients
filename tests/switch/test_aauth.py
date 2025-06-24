from nintendo.switch import aauth
from anynet import http
import pytest
import struct


TOKEN_REQUEST_1300 = (
	"POST /v3/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 1428\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"Expect: 100-continue\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&"
	"device_auth_token=device.token&media_type=DIGITAL&cert="
)

TOKEN_REQUEST_1500 = (
	"POST /v4/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 134\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&"
	"device_auth_token=device.token&media_type=DIGITAL&cert=token.from.dragons"
)

TOKEN_REQUEST_1800 = (
	"POST /v4/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 134\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&"
	"device_auth_token=device.token&media_type=DIGITAL&cert=token.from.dragons"
)

TOKEN_REQUEST_1900 = (
	"POST /v5/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 133\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&"
	"device_auth_token=device.token&auth_type=DIGITAL&cert=token.from.dragons"
)

CHALLENGE_REQUEST_1300 = (
	"POST /v3/challenge HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)\r\n"
	"Accept: */*\r\n"
	"Content-Length: 31\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"&device_auth_token=device.token"
)

CHALLENGE_REQUEST_1900 = (
	"POST /v5/challenge HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"Content-Length: 30\r\n\r\n"
	"device_auth_token=device.token"
)

CHALLENGE_REQUEST_2000 = (
	"POST /v5/challenge HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"Content-Length: 30\r\n\r\n"
	"device_auth_token=device.token"
)

GAMECARD_REQUEST_1300 = (
	"POST /v3/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)\r\n"
	"Accept: */*\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 132\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&device_auth_token=device.token&media_type=GAMECARD&gvt=Z3Z0&cert=Y2VydA"
)

GAMECARD_REQUEST_1900 = (
	"POST /v5/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 179\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&device_auth_token=device.token&auth_type=GAMECARD&gvt=Z3Z0&cert=Y2VydA&challenge=challenge&challenge_src=challenge_src"
)

GAMECARD_REQUEST_2000 = (
	"POST /v5/application_auth_token HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)\r\n"
	"Content-Type: application/x-www-form-urlencoded\r\n"
	"X-Nintendo-PowerState: FA\r\n"
	"Content-Length: 179\r\n\r\n"
	"application_id=0100123001234000&application_version=00070000&device_auth_token=device.token&auth_type=GAMECARD&gvt=Z3Z0&cert=Y2VydA&challenge=challenge&challenge_src=challenge_src"
)


CERT = struct.pack("<I", 0x10004) + bytes(0x29C)
CERT += struct.pack(">Q", 0x0100123001234000)
CERT += bytes(0x18)


@pytest.mark.anyio
async def test_aauth_1300():
	async def handler(client, request):
		text = request.encode().decode()
		assert text.startswith(TOKEN_REQUEST_1300)
		assert text[1375:1385] == "&cert_key="
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1300)
		client.set_context(None)
		response = await client.auth_digital(
			0x0100123001234000, 0x70000, "device.token", CERT
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_aauth_1500():
	async def handler(client, request):
		assert request.encode().decode() == TOKEN_REQUEST_1500
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.auth_digital(
			0x0100123001234000, 0x70000, "device.token", "token.from.dragons"
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_aauth_1800():
	async def handler(client, request):
		assert request.encode().decode() == TOKEN_REQUEST_1800
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1800)
		client.set_context(None)
		response = await client.auth_digital(
			0x0100123001234000, 0x70000, "device.token", "token.from.dragons"
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_aauth_1900():
	async def handler(client, request):
		assert request.encode().decode() == TOKEN_REQUEST_1900
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		response = await client.auth_digital(
			0x0100123001234000, 0x70000, "device.token", "token.from.dragons"
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_challenge_1300():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == CHALLENGE_REQUEST_1300
		response = http.HTTPResponse(200)
		response.json = {"seed": "seed", "value": "value"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1300)
		client.set_context(None)
		response = await client.challenge("device.token")
		assert response["seed"] == "seed"


@pytest.mark.anyio
async def test_challenge_1900():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == CHALLENGE_REQUEST_1900
		response = http.HTTPResponse(200)
		response.json = {
			"challenge": "challenge",
			"challenge_src": "challenge_src",
			"seed": "seed",
		}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		response = await client.challenge("device.token")
		assert response["seed"] == "seed"


@pytest.mark.anyio
async def test_challenge_2000():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == CHALLENGE_REQUEST_2000
		response = http.HTTPResponse(200)
		response.json = {
			"challenge": "challenge",
			"challenge_src": "challenge_src",
			"seed": "seed",
		}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.challenge("device.token")
		assert response["seed"] == "seed"


@pytest.mark.anyio
async def test_gamecard_1300():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == GAMECARD_REQUEST_1300
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1300)
		client.set_context(None)
		response = await client.auth_gamecard(
			0x0100123001234000, 0x70000, "device.token", b"cert", b"gvt"
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_gamecard_1900():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == GAMECARD_REQUEST_1900
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1900)
		client.set_context(None)
		response = await client.auth_gamecard(
			0x0100123001234000,
			0x70000,
			"device.token",
			b"cert",
			b"gvt",
			"challenge",
			"challenge_src",
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_gamecard_2000():
	async def handler(client, request):
		text = request.encode().decode()
		assert text == GAMECARD_REQUEST_2000
		response = http.HTTPResponse(200)
		response.json = {"application_auth_token": "application token"}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.auth_gamecard(
			0x0100123001234000,
			0x70000,
			"device.token",
			b"cert",
			b"gvt",
			"challenge",
			"challenge_src",
		)
		assert response["application_auth_token"] == "application token"


@pytest.mark.anyio
async def test_aauth_error():
	async def handler(client, request):
		response = http.HTTPResponse(400)
		response.json = {
			"errors": [{"code": "0118", "message": "Invalid parameter in request."}]
		}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = aauth.AAuthClient()
		client.set_host("localhost:12345")
		client.set_system_version(1500)
		client.set_context(None)
		with pytest.raises(aauth.AAuthError):
			await client.auth_nocert(0, 0, "device.token")
