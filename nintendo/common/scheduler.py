
import itertools
import anyio
import time


class Scheduler:
	def __init__(self, group):
		self.group = group
		
		self.handle = itertools.count()
		self.event = anyio.create_event()
		self.events = {}
		
	async def start(self):
		await self.group.spawn(self.process)
	
	async def process(self):
		while True:
			timeout = await self.process_timers()
			async with anyio.move_on_after(timeout):
				await self.event.wait()
				self.event = anyio.create_event()
	
	async def process_timers(self):
		minimum = None
		current = time.monotonic()
		items = self.events.copy().items()
		for handle, (deadline, repeat, function, args) in items:
			if deadline <= current:
				del self.events[handle]
				if repeat is not None:
					self.events[handle] = (deadline + repeat, repeat, function, args)
				await self.group.spawn(function, *args)
			else:
				if minimum is None or minimum > deadline - current:
					minimum = deadline - current
		return minimum
	
	async def schedule(self, function, timeout, *args):
		deadline = time.monotonic() + timeout
		
		handle = next(self.handle)
		self.events[handle] = (deadline, None, function, args)
		await self.event.set()
		return handle
	
	async def repeat(self, function, timeout, *args):
		deadline = time.monotonic() + timeout
		
		handle = next(self.handle)
		self.events[handle] = (deadline, timeout, function, args)
		await self.event.set()
		return handle
		
	def remove(self, handle):
		if handle in self.events:
			del self.events[handle]
