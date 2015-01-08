'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class InventoryAuthorizeRemoveRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.authorize_code = None
		self.sc_item_id = None
		self.user_nick_list = None

	def getapiname(self):
		return 'taobao.inventory.authorize.remove'
