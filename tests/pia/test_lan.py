
from nintendo.pia import lan, settings
import pytest

@pytest.mark.anyio
async def test_lan():
	def handler():
		info = lan.LanSessionInfo()
		info.game_mode = 1
		info.session_id = 100
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
		return [info]
	
	s = settings.Settings(50900, 0)
	async with lan.serve(s, handler, bytes(16)):
		crit = lan.LanSessionSearchCriteria()
		sessions = await lan.browse(s, crit, bytes(16), max=1)
		assert sessions[0].session_id == 100
