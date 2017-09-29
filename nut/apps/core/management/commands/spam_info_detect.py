# coding=utf-8
from __future__ import print_function

from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.core.models import User_Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        keywords = Command.get_keywords()
        keyword_filter = Q(bio='') | Q(nickname='')
        profiles = User_Profile.objects.filter(user__is_active__gt=0).exclude(keyword_filter).exclude(bio__isnull=True, nickname__isnull=True)
        profiles = profiles.order_by('-id')
        for profile in profiles:
            for keyword in keywords:
                if (profile.bio and keyword in profile.bio) or (profile.nickname and keyword in profile.nickname):
                    self.stdout.write(u'{},{}'.format(keyword, profile.id))

    @staticmethod
    def get_keywords():
        with open('data/keywords.txt') as f:
            keywords = [keyword.strip().decode('utf-8') for keyword in f]
            keywords = [keyword for keyword in keywords if keyword]
            return keywords
