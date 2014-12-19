# from django import forms
# from haystack.forms import SearchForm
# from django.utils.log import getLogger
#
# log = getLogger('django')
#
#
# class EntitySearchForm(SearchForm):
#     start_date = forms.DateField(required=False)
#     end_date = forms.DateField(required=False)
#
#     def search(self):
#         sqs = super(EntitySearchForm, self).search()
#         if not self.is_valid():
#             return self.no_query_found()
#
#         # if self.cleaned_data['start_date']:
#         #     sqs = sqs.filter(created_time__gte=self.cleaned_data['sta'])
#
#         return sqs
#
#
# __author__ = 'edison'
