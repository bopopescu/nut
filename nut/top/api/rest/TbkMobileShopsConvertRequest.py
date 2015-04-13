'''
Created by auto_sdk on 2015.04.13
'''
from top.api.base import RestApi
class TbkMobileShopsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.outer_code = None
		self.seller_nicks = None
		self.sids = None

	def getapiname(self):
		return 'taobao.tbk.mobile.shops.convert'
