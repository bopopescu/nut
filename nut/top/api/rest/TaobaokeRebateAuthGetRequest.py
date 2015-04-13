'''
Created by auto_sdk on 2015.04.13
'''
from top.api.base import RestApi
class TaobaokeRebateAuthGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.params = None
		self.type = None

	def getapiname(self):
		return 'taobao.taobaoke.rebate.auth.get'
