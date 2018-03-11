
import threading
import time

import logging
logger = logging.getLogger(__name__)


class Event:
	def __init__(self, callback, param):
		self.callback = callback
		self.param = param
		
	def trigger(self, *args):
		if self.param is None:
			self.callback(*args)
		else:
			self.callback(*args, self.param)
		
	def kill(self):
		if self in events:
			events.remove(self)
		
	def update(self): raise NotImplementedError("Event.update")


class Socket(Event):
	def __init__(self, callback, param, socket):
		super().__init__(callback, param)
		self.socket = socket
		
	def update(self):
		data = self.socket.recv()
		if data is not None:
			self.trigger(data)

		
class Timeout(Event):
	def __init__(self, callback, param, timeout, repeat=False):
		super().__init__(callback, param)
		self.timeout = timeout
		self.repeat = repeat

		self.reset()
		
	def update(self):
		if time.time() > self.deadline:
			self.trigger()
			if self.repeat:
				self.reset()
			else:
				self.kill()
				
	def reset(self):
		self.deadline = time.time() + self.timeout
		
		
thread = None
events = []

		
def add_socket(callback, socket, param=None):
	start_thread()
	event = Socket(callback, param, socket)
	events.append(event)
	return event

def add_timeout(callback, timeout, repeat=False, param=None):
	start_thread()
	event = Timeout(callback, param, timeout, repeat)
	events.append(event)
	return event
	
def remove(event):
	event.kill()

def start_thread():
	global thread
	if not thread:
		thread = threading.Thread(target=event_loop, daemon=True)
		thread.start()

def event_loop():
	while True:
		for event in events[:]:
			try:
				event.update()
			except:
				logger.error("An exception occurred while processing an event")
				import traceback
				traceback.print_exc()
				event.kill()
		time.sleep(0.02)
