'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class InventoryInitialItemRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.sc_item_id = None
		self.store_inventorys = None

	def getapiname(self):
		return 'taobao.inventory.initial.item'
