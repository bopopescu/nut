from apps.core.models import GKUser


def get_admin_user_choices():
    user_list = GKUser.objects.editor_or_admin()
    res = map(lambda x: (x.pk, x.profile.nickname), user_list)
    return res

__author__ = 'edison7500'
