# coding=utf-8

from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from math import ceil

class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


# class EmptyPage(InvalidPage):
#     pass


class ExtentPaginator(Paginator):

    def __init__(self, object_list, per_page ,range_num=5, *args, **kwargs ):
        super(ExtentPaginator, self).__init__(object_list, per_page,  *args, **kwargs )
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


class AnPaginator(ExtentPaginator):
    '''
    DO NOT USE !!!
    totally performance killer
    '''
    def page(self, number):
        self.page_num = number
        return super(ExtentPaginator, self).page(number)

    def _get_num_pages(self):
        """
        Retπurns the total number of pages.
        """
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """

        query = self.object_list.query
        key = 'count:cache:query:%s' % self.object_list.query
        count = cache.get(key)
        if not count is None:
            return int(count)

        if self._count is None:
            try:
                self._count = len(self.object_list)
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
        cache.set(key,self._count, timeout=3600*24)
        return self._count
    count = property(_get_count)


__author__ = 'edison'
