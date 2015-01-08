'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class HanoiActionGetSingleRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.action_code = None
		self.id = None
		self.name = None

	def getapiname(self):
		return 'taobao.hanoi.action.get.single'
