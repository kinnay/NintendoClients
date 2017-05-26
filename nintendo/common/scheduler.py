
import threading
import time
import _thread


class Scheduler:

	instance = None

	def __init__(self, interval=0.02):
		Scheduler.instance = self
		self.interval = interval
		self.tasks = []

	def start(self):
		self.stopping = False
		self.thread = threading.Thread(target=self.run)
		self.thread.setDaemon(True)
		self.thread.start()
		
	def stop(self):
		self.stopping = True
		
	def run(self):
		try:
			while not self.stopping:
				for task in self.tasks:
					task(self.interval)
				time.sleep(self.interval)
		except:
			import traceback
			traceback.print_exc()
			_thread.interrupt_main()
			
	def add(self, func):
		self.tasks.append(func)
		
	def remove(self, func):
		self.tasks.remove(func)
