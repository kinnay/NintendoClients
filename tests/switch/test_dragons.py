
from nintendo.switch import dragons
from anynet import http
import pytest


TEST_DEVICE_ID = 0x12345678
TEST_DEVICE_TOKEN = "device.token"
TEST_ELICENSE_ID = "337c8aaef372df9c2c239ebaaf49f723"
TEST_ACCOUNT_ID = 0x72b0f0bdb31753d5
TEST_APPLICATION_ID = 0x010040600C5CE000

PUBLISH_DEVICE_LINKED_ELICENSES_REQUEST = \
"""POST /v1/rights/publish_device_linked_elicenses HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: NintendoSDK Firmware/15.0.0-4.0 (platform:NX; did:0000000012345678; eid:lp1)
DeviceAuthorization: Bearer device.token
Content-Length: 0
Content-Type: application/x-www-form-urlencoded

"""

EXERCISE_ELICENSE_REQUEST = \
"""POST /v1/elicenses/exercise HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: NintendoSDK Firmware/15.0.0-4.0 (platform:NX; did:0000000012345678; eid:lp1)
DeviceAuthorization: Bearer device.token
Nintendo-Account-Id: 72b0f0bdb31753d5
Content-Type: application/json
Content-Length: 88

{"elicense_ids":["337c8aaef372df9c2c239ebaaf49f723"],"account_ids":["72b0f0bdb31753d5"]}"""

PUBLISH_ELICENSE_ARCHIVE_REQUEST_2301 = \
"""POST /v2/elicense_archives/publish HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: NintendoSDK Firmware/23.0.1-1.0 (platform:NX; did:0000000012345678; eid:lp1)
DeviceAuthorization: Bearer device.token
Nintendo-Account-Id: 72b0f0bdb31753d5
Content-Type: application/json
Content-Length: 57

{"challenge":"1be922884bbfc862","certificate":"dGVzdA=="}"""

REPORT_ELICENSE_ARCHIVE_REQUEST_2301 = \
"""PUT /v2/elicense_archives/337c8aaef372df9c2c239ebaaf49f723/report HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: NintendoSDK Firmware/23.0.1-1.0 (platform:NX; did:0000000012345678; eid:lp1)
DeviceAuthorization: Bearer device.token
Nintendo-Account-Id: 72b0f0bdb31753d5
Content-Length: 0

"""

AAUTH_TOKEN_REQUEST_1500 = \
"""POST /v1/contents_authorization_token_for_aauth/issue HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 15.3.0.0)
Accept: */*
Content-Type: application/json
DeviceAuthorization: Bearer device.token
Nintendo-Application-Id: 010040600c5ce000
Content-Length: 77

{"elicense_id":"337c8aaef372df9c2c239ebaaf49f723","na_id":"72b0f0bdb31753d5"}"""

AAUTH_TOKEN_REQUEST_1800 = \
"""POST /v1/contents_authorization_token_for_aauth/issue HTTP/1.1
Host: localhost:12345
Accept: */*
Content-Type: application/json
DeviceAuthorization: Bearer device.token
Nintendo-Application-Id: 010040600c5ce000
Content-Length: 77

{"elicense_id":"337c8aaef372df9c2c239ebaaf49f723","na_id":"72b0f0bdb31753d5"}"""

AAUTH_TOKEN_REQUEST_2000 = \
"""POST /v2/contents_authorization_token_for_aauth/issue HTTP/1.1
Host: localhost:12345
Accept: */*
User-Agent: libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)
Content-Type: application/json
DeviceAuthorization: Bearer device.token
Nintendo-Application-Id: 010040600c5ce000
Content-Length: 77

{"elicense_id":"337c8aaef372df9c2c239ebaaf49f723","na_id":"72b0f0bdb31753d5"}"""


@pytest.mark.anyio
async def test_publish_device_linked_elicenses():
	async def handler(client, request):
		assert request.encode().decode() == PUBLISH_DEVICE_LINKED_ELICENSES_REQUEST.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {"elicenses": []}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.publish_device_linked_elicenses(TEST_DEVICE_TOKEN)
		assert "elicenses" in response


@pytest.mark.anyio
async def test_exercise_elicense():
	async def handler(client, request):
		assert request.encode().decode() == EXERCISE_ELICENSE_REQUEST.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		await client.exercise_elicense(
			TEST_DEVICE_TOKEN, [TEST_ELICENSE_ID], [TEST_ACCOUNT_ID], TEST_ACCOUNT_ID
		)


@pytest.mark.anyio
async def test_publish_elicense_archive_2301():
	async def handler(client, request):
		assert request.encode().decode() == PUBLISH_ELICENSE_ARCHIVE_REQUEST_2301.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(2301)
		client.set_context(None)
		await client.publish_elicense_archive(
			TEST_DEVICE_TOKEN, "1be922884bbfc862", b"test", TEST_ACCOUNT_ID
		)


@pytest.mark.anyio
async def test_report_elicense_archive_2301():
	async def handler(client, request):
		assert request.encode().decode() == REPORT_ELICENSE_ARCHIVE_REQUEST_2301.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient(TEST_DEVICE_ID)
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(2301)
		client.set_context(None)
		await client.report_elicense_archive(
			TEST_DEVICE_TOKEN, TEST_ELICENSE_ID, TEST_ACCOUNT_ID
		)


@pytest.mark.anyio
async def test_contents_authorization_token_for_aauth_1500():
	async def handler(client, request):
		assert request.encode().decode() == AAUTH_TOKEN_REQUEST_1500.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"contents_authorization_token": "auth token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient()
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(1500)
		client.set_context(None)
		response = await client.contents_authorization_token_for_aauth(
			TEST_DEVICE_TOKEN, TEST_ELICENSE_ID, TEST_ACCOUNT_ID, TEST_APPLICATION_ID
		)
		assert response["contents_authorization_token"] == "auth token"


@pytest.mark.anyio
async def test_contents_authorization_token_for_aauth_1800():
	async def handler(client, request):
		assert request.encode().decode() == AAUTH_TOKEN_REQUEST_1800.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"contents_authorization_token": "auth token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient()
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(1800)
		client.set_context(None)
		response = await client.contents_authorization_token_for_aauth(
			TEST_DEVICE_TOKEN, TEST_ELICENSE_ID, TEST_ACCOUNT_ID, TEST_APPLICATION_ID
		)
		assert response["contents_authorization_token"] == "auth token"


@pytest.mark.anyio
async def test_contents_authorization_token_for_aauth_2000():
	async def handler(client, request):
		assert request.encode().decode() == AAUTH_TOKEN_REQUEST_2000.replace("\n", "\r\n")
		response = http.HTTPResponse(200)
		response.json = {
			"contents_authorization_token": "auth token"
		}
		return response
	
	async with http.serve(handler, "localhost", 12345):
		client = dragons.DragonsClient()
		client.set_hosts("localhost:12345", None, None)
		client.set_system_version(2000)
		client.set_context(None)
		response = await client.contents_authorization_token_for_aauth(
			TEST_DEVICE_TOKEN, TEST_ELICENSE_ID, TEST_ACCOUNT_ID, TEST_APPLICATION_ID
		)
		assert response["contents_authorization_token"] == "auth token"
