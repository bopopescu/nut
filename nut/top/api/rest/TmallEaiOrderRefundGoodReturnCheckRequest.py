'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class TmallEaiOrderRefundGoodReturnCheckRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.company_code = None
		self.confirm_result = None
		self.confirm_time = None
		self.operator = None
		self.refund_id = None
		self.refund_phase = None
		self.sid = None

	def getapiname(self):
		return 'tmall.eai.order.refund.good.return.check'
