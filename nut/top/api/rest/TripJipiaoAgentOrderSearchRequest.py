'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class TripJipiaoAgentOrderSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.begin_time = None
		self.end_time = None
		self.has_itinerary = None
		self.page = None
		self.status = None
		self.trip_type = None

	def getapiname(self):
		return 'taobao.trip.jipiao.agent.order.search'
