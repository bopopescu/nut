from django.forms import  ModelForm
from apps.notifications.models import DailyPush

class BaseDailyPushForm(ModelForm):
    class Meta:
        model =  DailyPush