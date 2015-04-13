'''
Created by auto_sdk on 2015.04.13
'''
from top.api.base import RestApi
class OpensecurityUidGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.tb_user_id = None

	def getapiname(self):
		return 'taobao.opensecurity.uid.get'
