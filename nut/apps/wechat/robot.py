from apps.wechat.models import RobotDic

class RobotHandler(object):
    def can_handle(self, keyword=None):
        if keyword is None:
            return False
        try:
            entry = RobotDic.objects.get(keyword=keyword)
        except (RobotDic.DoesNotExist, RobotDic.MultipleObjectsReturned) as e:
            return False

        return True

    def handle(self, keyword=None):
        if keyword is None:
            return False
        try:
            keyword = str(keyword).lower()
            entry = RobotDic.objects.get(keyword=keyword)
            return entry.resp
        except Exception as e :
            return None






