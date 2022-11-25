
from nintendo import five
from anynet import http
import contextlib
import pytest


UNREAD_INVITATION_COUNT_REQUEST = \
"""GET /v1/users/aaaaaaaaaaaaaaaa/invitations/inbox?fields=count&read=false HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access token

"""

GET_INBOX_REQUEST = \
"""GET /v1/users/aaaaaaaaaaaaaaaa/invitations/inbox HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access token

"""

GET_INVITATION_GROUP_REQUEST = \
"""GET /v1/invitation_groups/12345 HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access token

"""

MARK_ALL_AS_READ_REQUEST = \
"""PATCH /v1/users/aaaaaaaaaaaaaaaa/invitations/mark_as_read HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Authorization: Bearer access token
Content-Length: 0
Content-Type: application/x-www-form-urlencoded

"""

SEND_INVITATION_REQUEST = \
"""POST /v1/invitation_groups HTTP/1.1
Host: localhost:12345
User-Agent: libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)
Accept: */*
Content-Type: application/json
Authorization: Bearer access token
Content-Length: 241

{"receiver_ids":["bbbbbbbbbbbbbbbb"],"application_id":"010036b0034e4000","application_group_id":"010036b0034e4000","application_data":"YXBwbGljYXRpb24gZGF0YQ==","messages":{"ja":"\u4e00\u7dd2\u306b\u904a\u3073\u307e\u3057\u3087\u3046\uff01"},"application_id_match":false}"""


def check(handler, version):
	def decorator(callback):
		async def function():
			client = five.FiveClient()
			client.set_host("localhost:12345")
			client.set_system_version(version)
			client.set_context(None)
			async with http.serve(handler, "localhost", 12345):
				await callback(client)
		return pytest.mark.anyio(function)
	return decorator

def check_simple(version):
	async def handler(client, request):
		return http.HTTPResponse(200)
	return check(handler, version)

def check_request(expected_request, version, *, response={}):
	async def handler(client, request):
		request.json_options["ensure_ascii"] = False
		
		assert request.encode().decode() == expected_request.replace("\n", "\r\n")
		resp = http.HTTPResponse(200)
		resp.json = response
		return resp
	return check(handler, version)

@check_request(UNREAD_INVITATION_COUNT_REQUEST, 1501, response={"count": 0})
async def test_get_unread_invitation_count(client):
	await client.get_unread_invitation_count("access token", 0xaaaaaaaaaaaaaaaa)

@check_request(GET_INBOX_REQUEST, 1501)
async def test_get_inbox(client):
	await client.get_inbox("access token", 0xaaaaaaaaaaaaaaaa)

@check_request(GET_INVITATION_GROUP_REQUEST, 1501)
async def test_get_invitation_group(client):
	await client.get_invitation_group("access token", 12345)

@check_simple(1501)
async def test_mark_as_read(client):
	await client.mark_as_read("access token", [10000, 10001, 10002])

@check_request(MARK_ALL_AS_READ_REQUEST, 1501)
async def test_mark_all_as_read(client):
	await client.mark_all_as_read("access token", 0xaaaaaaaaaaaaaaaa)

@check_request(SEND_INVITATION_REQUEST, 1501)
async def test_send_invitation(client):
	receivers = [0xbbbbbbbbbbbbbbbb]
	title_id = 0x010036b0034e4000
	messages = {
		# Check if UTF-8 is handled correctly
		"ja": "\u4e00\u7dd2\u306b\u904a\u3073\u307e\u3057\u3087\u3046\uff01"
	}
	await client.send_invitation("access token", receivers, title_id, title_id, b"application data", messages)
