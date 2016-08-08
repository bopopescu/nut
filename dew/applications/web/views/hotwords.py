from applications.web import ListView
from applications.models.hotwords import HotWords



class HotWordsView(ListView):

    methods = ['get']

    def get_template_name(self):
        return 'web/hotwords/list.html'

    def get_objects(self):
        obj =  HotWords.query.all()
        return obj


class CreateHotWordView():
    pass
