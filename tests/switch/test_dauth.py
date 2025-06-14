
from nintendo.switch import dauth
from anynet import http
import pytest


CHALLENGE_REQUEST_1200 = \
	"POST /v6/challenge HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 17\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"key_generation=11"
	
CHALLENGE_REQUEST_1300 = \
	"POST /v7/challenge HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 17\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"key_generation=13"

CHALLENGE_REQUEST_1800 = \
	"POST /v7/challenge HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"Accept: */*\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 17\r\n\r\n" \
	"key_generation=17"

CHALLENGE_REQUEST_2000 = \
	"POST /v8/challenge HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"Accept: */*\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 17\r\n\r\n" \
	"key_generation=20"

TOKEN_REQUEST_1200 = \
	"POST /v6/device_auth_token HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 211\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"challenge=vaNgVZZH7gUse0y3t8Cksuln-TAVtvBmcD-ow59qp0E=&" \
	"client_id=8f849b5d34778d8e&ist=false&key_generation=11&" \
	"system_version=CusHY#000c0000#C-BynYNPXdQJNBZjx02Hizi8lRUSIKLwPGa5p8EY1uo=&" \
	"mac=xRB_6mgnNqrnF9DRsEpYMg"
	
DEVICE_TOKEN_REQUEST_1300 = \
	"POST /v7/device_auth_token HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 211\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n\r\n" \
	"challenge=TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=&" \
	"client_id=8f849b5d34778d8e&ist=false&key_generation=13&" \
	"system_version=CusHY#000d0000#r1xneESd4PiTRYIhVIl0bK1ST5L5BUmv_uGPLqc4PPo=&" \
	"mac=dGMjt0ShsDr-uNrsHtCB1g"

DEVICE_TOKEN_REQUEST_1800 = \
	"POST /v7/device_auth_token HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"Accept: */*\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 211\r\n\r\n" \
	"challenge=TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=&" \
	"client_id=8f849b5d34778d8e&ist=false&key_generation=17&" \
	"system_version=CusHY#00120000#U531L4Si9RbhOVeyVppe18WHkJ0k4_KzrNtygsekMNo=&" \
	"mac=c4SgqSjdfdNFoRM35ChrLw"

DEVICE_TOKEN_REQUEST_2000 = \
	"POST /v8/device_auth_tokens HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"Accept: */*\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)\r\n" \
	"Content-Type: application/json\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 293\r\n\r\n" \
	'{"system_version":"00140000","fw_revision":"7147e1386c9b6c15d8f14e6ed68c4b9a7f28fb9b","ist":false,"token_requests":[{"client_id":"8f849b5d34778d8e"},{"client_id":"dc656ea03b63cf68"}],"key_generation":20,"challenge":"TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=","mac":"49YDQDn9UTq6iQGMdW5B8Q"}'

EDGE_TOKEN_REQUEST_2000 = \
	"POST /v8/edge_tokens HTTP/1.1\r\n" \
	"Host: localhost:12345\r\n" \
	"Accept: */*\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)\r\n" \
	"Content-Type: application/json\r\n" \
	"X-Nintendo-PowerState: FA\r\n" \
	"Content-Length: 335\r\n\r\n" \
	'{"system_version":"00140000","fw_revision":"7147e1386c9b6c15d8f14e6ed68c4b9a7f28fb9b","ist":false,"token_requests":[{"client_id":"93af0acb26258de9","vendor_id":"akamai"},{"client_id":"67bf9945b45248c6","vendor_id":"akamai"}],"key_generation":20,"challenge":"TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=","mac":"bB8LFaSTRsZtrWQD9Ew1-Q"}'


@pytest.mark.anyio
async def test_dauth_1200():
	async def handler(client, request):
		if request.path == "/v6/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST_1200
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "vaNgVZZH7gUse0y3t8Cksuln-TAVtvBmcD-ow59qp0E=",
				"data": "dlL7ZBNSLmYo1hUlKYZiUA=="
			}
			return response
		else:
			assert request.encode().decode() == TOKEN_REQUEST_1200
			response = http.HTTPResponse(200)
			response.json = {
				"device_auth_token": "device token"
			}
			return response
	
	async with http.serve(handler, "localhost", 12345):
		keys = {
			"aes_kek_generation_source": bytes.fromhex("485d45ad27c07c7e538c0183f90ee845"),
			"master_key_0a": bytes.fromhex("37eed242e0f2ce6f8371e783c1a6a0ae")
		}
		
		client = dauth.DAuthClient(keys)
		client.set_host("localhost:12345")
		client.set_system_version(1200)
		client.set_context(None)
		response = await client.device_token(dauth.CLIENT_ID_BAAS)
		token = response["device_auth_token"]
		assert token == "device token"

@pytest.mark.anyio
async def test_dauth_1300():
	async def handler(client, request):
		if request.path == "/v7/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST_1300
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=",
				"data": "4SxW91vqVg6pz4CXMH2Ouw=="
			}
			return response
		else:
			assert request.encode().decode() == DEVICE_TOKEN_REQUEST_1300
			response = http.HTTPResponse(200)
			response.json = {
				"device_auth_token": "device token"
			}
			return response
	
	async with http.serve(handler, "localhost", 12345):
		keys = {
			"aes_kek_generation_source": bytes.fromhex("cae2728f56af642d5d59dfc23bd314a2"),
			"master_key_0c": bytes.fromhex("f1642c98bddb5850eb23d0cebab7dc05")
		}
		
		client = dauth.DAuthClient(keys)
		client.set_host("localhost:12345")
		client.set_system_version(1300)
		client.set_context(None)
		response = await client.device_token(dauth.CLIENT_ID_BAAS)
		token = response["device_auth_token"]
		assert token == "device token"

@pytest.mark.anyio
async def test_dauth_1800():
	async def handler(client, request):
		if request.path == "/v7/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST_1800
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=",
				"data": "4SxW91vqVg6pz4CXMH2Ouw=="
			}
			return response
		else:
			assert request.encode().decode() == DEVICE_TOKEN_REQUEST_1800
			response = http.HTTPResponse(200)
			response.json = {
				"device_auth_token": "device token"
			}
			return response
	
	async with http.serve(handler, "localhost", 12345):
		keys = {
			"aes_kek_generation_source": bytes.fromhex("1092ce3d2c208c250ebe248537f2df73"),
			"master_key_10": bytes.fromhex("2fcb5dd5355a220a12eaeb8069bb75e1")
		}
		
		client = dauth.DAuthClient(keys)
		client.set_host("localhost:12345")
		client.set_system_version(1800)
		client.set_context(None)
		response = await client.device_token(dauth.CLIENT_ID_BAAS)
		token = response["device_auth_token"]
		assert token == "device token"

@pytest.mark.anyio
async def test_dauth_2000():
	async def handler(client, request):
		if request.path == "/v8/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST_2000
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=",
				"data": "4SxW91vqVg6pz4CXMH2Ouw=="
			}
			return response
		else:
			assert request.encode().decode() == DEVICE_TOKEN_REQUEST_2000
			return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		keys = {
			"aes_kek_generation_source": bytes.fromhex("1092ce3d2c208c250ebe248537f2df73"),
			"master_key_13": bytes.fromhex("f09f742cf07cceb584410e13c507e27e")
		}
		
		client = dauth.DAuthClient(keys)
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		await client.device_tokens([
			dauth.CLIENT_ID_BAAS,
			dauth.CLIENT_ID_PCTL
		])

@pytest.mark.anyio
async def test_edge_token_2000():
	async def handler(client, request):
		if request.path == "/v8/challenge":
			assert request.encode().decode() == CHALLENGE_REQUEST_2000
			response = http.HTTPResponse(200)
			response.json = {
				"challenge": "TzJ0EB3EvsWvQI5aPj15uaNVH9paGdsWB4l-eI5uzW0=",
				"data": "4SxW91vqVg6pz4CXMH2Ouw=="
			}
			return response
		else:
			assert request.encode().decode() == EDGE_TOKEN_REQUEST_2000
			return http.HTTPResponse(200)
	
	async with http.serve(handler, "localhost", 12345):
		keys = {
			"aes_kek_generation_source": bytes.fromhex("1092ce3d2c208c250ebe248537f2df73"),
			"master_key_13": bytes.fromhex("f09f742cf07cceb584410e13c507e27e")
		}
		
		client = dauth.DAuthClient(keys)
		client.set_host("localhost:12345")
		client.set_system_version(2000)
		client.set_context(None)
		await client.edge_tokens([
			(dauth.CLIENT_ID_BEACH, "akamai"),
			(dauth.CLIENT_ID_BCAT, "akamai")
		])

@pytest.mark.anyio
async def test_dauth_error():
	async def handler(client, request):
		response = http.HTTPResponse(400)
		response.json = {
			"errors": [{"code": "0014", "message": "Invalid parameter in request."}]
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dauth.DAuthClient({})
		client.set_host("localhost:12345")
		client.set_system_version(1300)
		client.set_context(None)
		try:
			await client.challenge()
		except dauth.DAuthError as e:
			assert e.code == dauth.DAuthError.GENERIC
		else:
			pytest.fail("DAuth client should have raised an exception")
