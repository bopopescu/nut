from apps.core.models import GKUser, Category


def get_author_choices():
    author_list = list(
                    set(
                        list(GKUser.objects.author())
                         # list(GKUser.objects.authorized_author())
                        )
                    )
    res = map(lambda x: (x.pk, x.profile.nickname), author_list)
    return res

def get_admin_user_choices():
    user_list = GKUser.objects.editor()
    res = map(lambda x: (x.pk, x.profile.nickname), user_list)
    return res

def get_category_choices():
    category_list = Category.objects.filter(status=True)
    res = map(lambda x : (x.id, x.title), category_list)
    return res


__author__ = 'edison7500'
