'''
Created by auto_sdk on 2015.04.13
'''
from top.api.base import RestApi
class TbkMobileItemsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.num_iids = None
		self.outer_code = None

	def getapiname(self):
		return 'taobao.tbk.mobile.items.convert'
