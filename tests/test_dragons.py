
from nintendo import dragons
from anynet import http
import pytest


TEST_DEVICE_ID = 0x12345678
TEST_DEVICE_TOKEN = "device.token"
TEST_ELICENSE_ID = "337c8aaef372df9c2c239ebaaf49f723"
TEST_ACCOUNT_ID = 0x72b0f0bdb31753d5
TEST_APPLICATION_ID = 0x010040600C5CE000

PUBLISH_DEVICE_LINKED_ELICENSES_REQUEST = \
	"POST /v1/rights/publish_device_linked_elicenses HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"Accept: */*\r\n" \
	"User-Agent: NintendoSDK Firmware/15.0.0-4.0 (platform:NX; did:0000000012345678; eid:lp1)\r\n" \
	"DeviceAuthorization: Bearer device.token\r\n" \
	"Content-Length: 0\r\n" \
	"Content-Type: application/x-www-form-urlencoded\r\n" \
	"\r\n"

EXERCISE_ELICENSE_REQUEST = \
	"POST /v1/elicenses/exercise HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"Accept: */*\r\n" \
	"User-Agent: NintendoSDK Firmware/15.0.0-4.0 (platform:NX; did:0000000012345678; eid:lp1)\r\n" \
	"DeviceAuthorization: Bearer device.token\r\n" \
	"Nintendo-Account-Id: 72b0f0bdb31753d5\r\n" \
	"Content-Type: application/json\r\n" \
	"Content-Length: 88\r\n" \
	"\r\n" \
	'{"elicense_ids":["337c8aaef372df9c2c239ebaaf49f723"],"account_ids":["72b0f0bdb31753d5"]}'

AAUTH_TOKEN_REQUEST = \
	"POST /v1/contents_authorization_token_for_aauth/issue HTTP/1.1\r\n" \
	"Host: 127.0.0.1:12345\r\n" \
	"User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 15.3.0.0)\r\n" \
	"Accept: */*\r\n" \
	"Content-Type: application/json\r\n" \
	"DeviceAuthorization: Bearer device.token\r\n" \
	"Nintendo-Application-Id: 010040600c5ce000\r\n" \
	"Content-Length: 77\r\n" \
	"\r\n" \
	'{"elicense_id":"337c8aaef372df9c2c239ebaaf49f723","na_id":"72b0f0bdb31753d5"}'


@pytest.mark.anyio
async def test_publish_device_linked_elicenses():
	async def handler(client, request):
		assert request.encode().decode() == PUBLISH_DEVICE_LINKED_ELICENSES_REQUEST
		response = http.HTTPResponse(200)
		response.json = {"elicenses": []}
		return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("127.0.0.1:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.publish_device_linked_elicenses(TEST_DEVICE_TOKEN)
		assert "elicenses" in response


@pytest.mark.anyio
async def test_exercise_elicense():
	async def handler(client, request):
		assert request.encode().decode() == EXERCISE_ELICENSE_REQUEST
		response = http.HTTPResponse(200)
		return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("127.0.0.1:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		await client.exercise_elicense(
			TEST_DEVICE_TOKEN, [TEST_ELICENSE_ID], [TEST_ACCOUNT_ID], TEST_ACCOUNT_ID
		)


@pytest.mark.anyio
async def test_contents_authorization_token_for_aauth():
	async def handler(client, request):
		assert request.encode().decode() == AAUTH_TOKEN_REQUEST
		response = http.HTTPResponse(200)
		response.json = {
			"contents_authorization_token": "auth token"
		}
		return response
	
	async with http.serve(handler, "127.0.0.1", 12345):
		client = dragons.DragonsClient()
		client.set_hosts("127.0.0.1:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.contents_authorization_token_for_aauth(
			TEST_DEVICE_TOKEN, TEST_ELICENSE_ID, TEST_ACCOUNT_ID, TEST_APPLICATION_ID
		)
		assert response["contents_authorization_token"] == "auth token"
