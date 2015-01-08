'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class IncrementItemsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_modified = None
		self.nick = None
		self.page_no = None
		self.page_size = None
		self.start_modified = None
		self.status = None

	def getapiname(self):
		return 'taobao.increment.items.get'
