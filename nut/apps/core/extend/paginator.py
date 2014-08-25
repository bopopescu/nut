from django.core.paginator import Paginator


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class ExtentPaginator(Paginator):

    def __init__(self, object_list, per_page, range_num=5):
        super(ExtentPaginator, self).__init__(object_list, per_page)
        self.range_num = range_num


    def page(self, number):
        self.page_num = self.validate_number(number)
        return super(ExtentPaginator, self).page(number)


    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
              return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)
            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)

        num_list.sort()
        return num_list
    page_range_ext = property(_page_range_ext)


__author__ = 'edison'
