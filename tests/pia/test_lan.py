
from nintendo.pia import lan, settings
import pytest


def make_session_info(session_id):
	info = lan.LanSessionInfo()
	info.game_mode = 1
	info.session_id = session_id
	info.attributes = [0, 1, 2, 3, 4, 5]
	info.num_participants = 1
	info.min_participants = 1
	info.max_participants = 4
	info.system_version = 10
	info.application_version = 35
	info.session_type = 1
	info.application_data = b""
	info.is_opened = True
	info.session_param = bytes(32)
	return info


@pytest.mark.anyio
async def test_browse():
	def handler():
		return [make_session_info(100)]
	
	s = settings.Settings(50900, 0)
	async with lan.serve(s, handler, bytes(16)):
		crit = lan.LanSessionSearchCriteria()
		sessions = await lan.browse(s, crit, bytes(16), max=1)
		assert len(sessions) == 1
		assert sessions[0].session_id == 100


@pytest.mark.anyio
async def test_browse_max():
	def handler():
		return [make_session_info(100), make_session_info(101)]
	
	s = settings.Settings(50900, 0)
	async with lan.serve(s, handler, bytes(16)):
		crit = lan.LanSessionSearchCriteria()
		sessions = await lan.browse(s, crit, bytes(16), max=2)
		assert len(sessions) == 2
		
		ids = set(session.session_id for session in sessions)
		assert ids == {100, 101}
