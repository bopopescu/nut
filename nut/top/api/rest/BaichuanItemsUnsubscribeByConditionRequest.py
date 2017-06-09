'''
Created by auto_sdk on 2016.08.04
'''
from top.api.base import RestApi
class BaichuanItemsUnsubscribeByConditionRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.condition = None

	def getapiname(self):
		return 'taobao.baichuan.items.unsubscribe.by.condition'
