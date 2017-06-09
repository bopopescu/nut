'''
Created by auto_sdk on 2017.02.23
'''
from top.api.base import RestApi
class ItemDetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.item_id = None
		self.params = None

	def getapiname(self):
		return 'taobao.item.detail.get'
