from nintendo.switch import sun
from anynet import http
import pytest


TEST_DEVICE_ID = 0x6265CA40780B1C0D

SYSTEM_UPDATE_META_REQUEST = (
	"GET /v1/system_update_meta?device_id=6265ca40780b1c0d HTTP/1.1\r\n"
	"Host: localhost:12345\r\n"
	"User-Agent: NintendoSDK Firmware/17.0.0-6.0 (platform:NX; did:6265ca40780b1c0d; eid:lp1)\r\n"
	"Accept: application/json\r\n"
	"\r\n"
)


@pytest.mark.anyio
async def test_system_update_meta():
	async def handler(client, request):
		assert request.encode().decode() == SYSTEM_UPDATE_META_REQUEST
		response = http.HTTPResponse(200)
		response.json = {"system_update_metas": []}
		return response

	async with http.serve(handler, "localhost", 12345):
		client = sun.SunClient(TEST_DEVICE_ID)
		client.set_host("localhost:12345")
		client.set_system_version(1700)
		client.set_context(None)
		response = await client.system_update_meta()
		assert "system_update_metas" in response
