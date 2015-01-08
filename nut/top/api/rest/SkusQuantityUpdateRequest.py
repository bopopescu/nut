'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class SkusQuantityUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.num_iid = None
		self.outerid_quantities = None
		self.skuid_quantities = None
		self.type = None

	def getapiname(self):
		return 'taobao.skus.quantity.update'
