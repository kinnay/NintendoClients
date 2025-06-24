from nintendo.switch import atumn
from anynet import http
import pytest


TEST_DEVICE_ID = 0x6265CA40780B1C0D
TEST_SYSTEM_UPDATE_TITLE_ID = 0x0100000000000816
TEST_SYSTEM_UPDATE_TITLE_VERSION = 1140851708
TEST_TITLE_ID = 0x0100000000000006
TEST_TITLE_VERSION = 1140851648
TEST_CONTENT_ID = "e3a44d36db9756202bef1dcd3bfb65ef"

SYSTEM_UPDATE_HEAD_REQUEST = (
	"HEAD /t/s/0100000000000816/1140851708?device_id=6265ca40780b1c0d HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"\r\n"
)

SYSTEM_UPDATE_GET_REQUEST = (
	"GET /c/s/170ca33980ff8e9cdad31c6add0f38b6 HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"\r\n"
)

SYSTEM_TITLE_HEAD_REQUEST = (
	"HEAD /t/a/0100000000000006/1140851648?device_id=6265ca40780b1c0d HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"\r\n"
)

SYSTEM_TITLE_GET_REQUEST = (
	"GET /c/a/aa4c1492ab0ab849fbc1002eb3ecc784 HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"\r\n"
)

CONTENT_REQUEST = (
	"GET /c/c/e3a44d36db9756202bef1dcd3bfb65ef HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"Accept: */*\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"\r\n"
)


@pytest.mark.anyio
async def test_download_content_metadata_system_update():
	async def handler(client, request):
		data = request.encode().decode()
		if data == SYSTEM_UPDATE_HEAD_REQUEST:
			response = http.HTTPResponse(200)
			response.headers = {
				"X-Nintendo-Content-ID": "170ca33980ff8e9cdad31c6add0f38b6"
			}
			return response
		elif data == SYSTEM_UPDATE_GET_REQUEST:
			response = http.HTTPResponse(200)
			response.body = b"test data"
			return response
		else:
			raise ValueError("Incorrect request")

	async with http.serve(handler, "localhost", 12345):
		client = atumn.AtumnClient(TEST_DEVICE_ID)
		client.set_host("localhost:12345")
		client.set_system_version(1700)
		client.set_context(None)
		response = await client.download_content_metadata(
			TEST_SYSTEM_UPDATE_TITLE_ID,
			TEST_SYSTEM_UPDATE_TITLE_VERSION,
			system_update=True,
		)
		assert response == b"test data"


@pytest.mark.anyio
async def test_download_content_metadata_normal_title():
	async def handler(client, request):
		data = request.encode().decode()
		if data == SYSTEM_TITLE_HEAD_REQUEST:
			response = http.HTTPResponse(200)
			response.headers = {
				"X-Nintendo-Content-ID": "aa4c1492ab0ab849fbc1002eb3ecc784"
			}
			return response
		elif data == SYSTEM_TITLE_GET_REQUEST:
			response = http.HTTPResponse(200)
			response.body = b"test data"
			return response
		else:
			raise ValueError("Incorrect request")

	async with http.serve(handler, "localhost", 12345):
		client = atumn.AtumnClient(TEST_DEVICE_ID)
		client.set_host("localhost:12345")
		client.set_system_version(1700)
		client.set_context(None)
		response = await client.download_content_metadata(
			TEST_TITLE_ID, TEST_TITLE_VERSION
		)
		assert response == b"test data"


@pytest.mark.anyio
async def test_download_content():
	async def handler(client, request):
		data = request.encode().decode()
		assert data == CONTENT_REQUEST

		response = http.HTTPResponse(200)
		response.body = b"test data"
		return response

	async with http.serve(handler, "localhost", 12345):
		client = atumn.AtumnClient(TEST_DEVICE_ID)
		client.set_host("localhost:12345")
		client.set_system_version(1700)
		client.set_context(None)
		response = await client.download_content(TEST_CONTENT_ID)
		assert response == b"test data"
