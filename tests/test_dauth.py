
from nintendo import dauth, switch
from anynet import http
import pytest


CHALLENGE_REQUEST = \
	"POST /v6/challenge HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 17\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"key_generation=11"

TOKEN_REQUEST = \
	"POST /v6/device_auth_token HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 211\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"challenge=vaNgVZZH7gUse0y3t8Cksuln-TAVtvBmcD-ow59qp0E=&" \
	"client_id=8f849b5d34778d8e&ist=false&key_generation=11&" \
	"system_version=CusHY#000c0000#C-BynYNPXdQJNBZjx02Hizi8lRUSIKLwPGa5p8EY1uo=&" \
	"mac=xRB_6mgnNqrnF9DRsEpYMg"


@pytest.mark.anyio
async def test_dauth():
	async def handler(client, request):
		if request.path == "/v6/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "vaNgVZZH7gUse0y3t8Cksuln-TAVtvBmcD-ow59qp0E=",
				"data": "dlL7ZBNSLmYo1hUlKYZiUA=="
			}
			return response
		else:
			assert request.encode().decode() == TOKEN_REQUEST
			response = http.HTTPResponse(200)
			response.json = {
				"device_auth_token": "device token"
			}
			return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		keys = switch.KeySet()
		keys["aes_kek_generation_source"] = bytes.fromhex("485d45ad27c07c7e538c0183f90ee845")
		keys["master_key_0a"] = bytes.fromhex("37eed242e0f2ce6f8371e783c1a6a0ae")
		client = dauth.DAuthClient(keys)
		client.set_url("127.0.0.1:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.device_token(client.BAAS)
		token = response["device_auth_token"]
		assert token == "device token"
