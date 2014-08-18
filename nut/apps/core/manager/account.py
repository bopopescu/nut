from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# import random


class GKUserQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def deactive(self):
        return self.filter(is_active=False)

    def admin(self):
        return self.filter(is_admin=True)


class GKUserManager(BaseUserManager):

    def get_query_set(self):
        return GKUserQuerySet(self.model, using = self._db)

    def active(self):
        return self.get_query_set().active()

    def deactive(self):
        return self.get_query_set().deactive()

    def admin(self):
        return self.get_query_set().admin()

    def _create_user(self, email, password, is_active, is_admin, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('please given cellphone number'))

        user = self.model(email=email, is_active=is_active, is_admin=is_admin, date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, is_active=True, **extra_fields):

        is_admin = extra_fields.pop("is_admin", False)
        return self._create_user(email, password, is_active, is_admin, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

__author__ = 'edison7500'
