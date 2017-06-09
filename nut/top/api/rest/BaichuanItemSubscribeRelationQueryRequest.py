'''
Created by auto_sdk on 2016.08.04
'''
from top.api.base import RestApi
class BaichuanItemSubscribeRelationQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None

	def getapiname(self):
		return 'taobao.baichuan.item.subscribe.relation.query'
