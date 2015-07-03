'''
Created by auto_sdk on 2015.07.02
'''
from top.api.base import RestApi
class SpContentGraphicUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.classname = None
		self.contents = None
		self.coverpicurl = None
		self.detailurl = None
		self.id = None
		self.intimeline = None
		self.site_key = None
		self.tags = None
		self.title = None

	def getapiname(self):
		return 'taobao.sp.content.graphic.update'
