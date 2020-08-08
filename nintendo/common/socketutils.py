
import anyio


class PacketQueue:
	def __init__(self):
		self.queue = []
		self.busy = False
		self.closed = False
		self.event = None
	
	async def get(self):
		if self.event:
			raise anyio.exceptions.ResourceBusyError
		
		while True:
			if self.queue:
				return self.queue.pop(0)
			if self.closed:
				raise anyio.exceptions.ClosedResourceError
			
			self.event = anyio.create_event()
			await self.event.wait()
			self.event = None
	
	async def put(self, item):
		if self.closed:
			raise anyio.exceptions.ClosedResourceError
		self.queue.append(item)
		if self.event:
			await self.event.set()
	
	async def close(self):
		self.closed = True
		if self.event:
			await self.event.set()
