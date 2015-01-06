from apps.core.models import GKUser, Category


def get_admin_user_choices():
    user_list = GKUser.objects.editor_or_admin()
    res = map(lambda x: (x.pk, x.profile.nickname), user_list)
    return res

def get_category_choices():

    category_list = Category.objects.all()
    # log.info(category_list)
    res = map(lambda x : (x.id, x.title), category_list)
    return res



__author__ = 'edison7500'
