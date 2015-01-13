from apps.core.utils.http import SuccessJsonResponse

from apps.core.models import Category, Sub_Category


def list(request):

    categories = Category.objects.all()
    res = []
    for category in categories:
        res.append(
            {
                'group_id' : category.id,
                'title' : category.title,
                'status' : category.status,
                'category_count': category.sub_category_count,
            }
        )


    return SuccessJsonResponse(res)


__author__ = 'edison'
