from django.forms import ModelForm
from apps.wechat.models import RobotDic

class BaseKeywordForm(ModelForm):
    class Meta:
        model = RobotDic


