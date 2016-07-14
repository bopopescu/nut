

class BaseRequestApi():
    def __init__(self, protocol='https://', url='openapi.alipay.com/gateway.do', port=80):
        self.__protocol = protocol
        self.__port = port
        self.__httpmethod = "POST"
