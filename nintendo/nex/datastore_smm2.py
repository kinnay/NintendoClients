
# This file was generated automatically from datastore_smm2.proto

from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class GetUserOrCourseParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.code = None
		self.user_option = None
		self.course_option = None
	
	def check_required(self, settings):
		for field in ['code', 'user_option', 'course_option']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.code = stream.string()
		self.user_option = stream.u32()
		self.course_option = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.code)
		stream.u32(self.user_option)
		stream.u32(self.course_option)


class DataStoreSMM2Protocol:
	
	PROTOCOL_ID = 0x0


class DataStoreSMM2Client(DataStoreSMM2Protocol):
	def __init__(self, client):
		self.client = client


class DataStoreSMM2Server(DataStoreSMM2Protocol):
	def __init__(self):
		self.methods = {
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on DataStoreSMM2Server: %i", method_id)
			raise common.RMCError("Core::NotImplemented")

