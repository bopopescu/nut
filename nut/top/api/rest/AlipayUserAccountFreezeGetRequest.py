'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class AlipayUserAccountFreezeGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.freeze_type = None

	def getapiname(self):
		return 'alipay.user.account.freeze.get'
