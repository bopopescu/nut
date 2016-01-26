from django.db.models import Model, TextField , DateTimeField
from django.utils import timezone

class SogouCookies(Model):
    cookie_string = TextField()
    created_time = DateTimeField(default=timezone.now())
    class Meta:
        ordering = ['-created_time']

