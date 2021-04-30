
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class SubscriberProtocol:
	METHOD_HELLO = 1
	METHOD_POST_CONTENT = 2
	METHOD_GET_CONTENT = 3
	METHOD_FOLLOW = 4
	METHOD_UNFOLLOW_ALL_AND_FOLLOW = 5
	METHOD_UNFOLLOW = 6
	METHOD_GET_FOLLOWING = 7
	METHOD_GET_FOLLOWER = 8
	METHOD_GET_NUM_FOLLOWERS = 9
	METHOD_GET_TIMELINE = 10
	METHOD_DELETE_CONTENT = 11
	METHOD_GET_CONTENT_MULTI = 12
	METHOD_UPDATE_USER_STATUS = 13
	METHOD_GET_FRIEND_USER_STATUSES = 14
	METHOD_GET_USER_STATUSES = 15
	
	PROTOCOL_ID = 0x79


class SubscriberClient(SubscriberProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	


class SubscriberServer(SubscriberProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_HELLO: self.handle_hello,
			self.METHOD_POST_CONTENT: self.handle_post_content,
			self.METHOD_GET_CONTENT: self.handle_get_content,
			self.METHOD_FOLLOW: self.handle_follow,
			self.METHOD_UNFOLLOW_ALL_AND_FOLLOW: self.handle_unfollow_all_and_follow,
			self.METHOD_UNFOLLOW: self.handle_unfollow,
			self.METHOD_GET_FOLLOWING: self.handle_get_following,
			self.METHOD_GET_FOLLOWER: self.handle_get_follower,
			self.METHOD_GET_NUM_FOLLOWERS: self.handle_get_num_followers,
			self.METHOD_GET_TIMELINE: self.handle_get_timeline,
			self.METHOD_DELETE_CONTENT: self.handle_delete_content,
			self.METHOD_GET_CONTENT_MULTI: self.handle_get_content_multi,
			self.METHOD_UPDATE_USER_STATUS: self.handle_update_user_status,
			self.METHOD_GET_FRIEND_USER_STATUSES: self.handle_get_friend_user_statuses,
			self.METHOD_GET_USER_STATUSES: self.handle_get_user_statuses,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on SubscriberServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_hello(self, client, input, output):
		logger.warning("SubscriberServer.hello is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_post_content(self, client, input, output):
		logger.warning("SubscriberServer.post_content is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_content(self, client, input, output):
		logger.warning("SubscriberServer.get_content is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_follow(self, client, input, output):
		logger.warning("SubscriberServer.follow is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_unfollow_all_and_follow(self, client, input, output):
		logger.warning("SubscriberServer.unfollow_all_and_follow is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_unfollow(self, client, input, output):
		logger.warning("SubscriberServer.unfollow is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_following(self, client, input, output):
		logger.warning("SubscriberServer.get_following is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_follower(self, client, input, output):
		logger.warning("SubscriberServer.get_follower is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_num_followers(self, client, input, output):
		logger.warning("SubscriberServer.get_num_followers is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_timeline(self, client, input, output):
		logger.warning("SubscriberServer.get_timeline is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_delete_content(self, client, input, output):
		logger.warning("SubscriberServer.delete_content is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_content_multi(self, client, input, output):
		logger.warning("SubscriberServer.get_content_multi is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_update_user_status(self, client, input, output):
		logger.warning("SubscriberServer.update_user_status is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_friend_user_statuses(self, client, input, output):
		logger.warning("SubscriberServer.get_friend_user_statuses is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_user_statuses(self, client, input, output):
		logger.warning("SubscriberServer.get_user_statuses is not supported")
		raise common.RMCError("Core::NotImplemented")

