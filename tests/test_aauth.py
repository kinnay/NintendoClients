
from nintendo import aauth
from anynet import http
import pytest
import struct


TOKEN_REQUEST_1300 = \
	"POST /v3/application_auth_token HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 1428\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"Expect: 100-continue\r\n\r\n" \
	"application_id=0100123001234000&application_version=00070000&" \
	"device_auth_token=device.token&media_type=DIGITAL&cert="

TOKEN_REQUEST_1500 = \
	"POST /v4/application_auth_token HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 134\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"application_id=0100123001234000&application_version=00070000&" \
	"device_auth_token=device.token&media_type=DIGITAL&cert=token.from.dragons"


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
		response.json = {
			"application_auth_token": "application token"
		}
		return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = aauth.AAuthClient()
		client.set_host("127.0.0.1:12345")
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
		response.json = {
			"application_auth_token": "application token"
		}
		return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = aauth.AAuthClient()
		client.set_host("127.0.0.1:12345")
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.auth_digital(
			0x0100123001234000, 0x70000, "device.token", "token.from.dragons"
		)
		assert response["application_auth_token"] == "application token"
