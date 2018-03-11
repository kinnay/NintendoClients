
import time

TIMER_SPEED = 248625000 // 4

base_time = time.monotonic()
def OSGetSystemTime():
	time_diff = time.monotonic() - base_time
	return int(TIMER_SPEED * time_diff)
