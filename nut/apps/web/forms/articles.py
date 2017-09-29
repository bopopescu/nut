from django.forms import ModelForm

from apps.core.models import Article


class WebArticleEditForm(ModelForm):
    def clean_showcover(self):
        # TODO , fix this before open to the public
        # we should not use user input data directly , never !!!!
        #
        if int(self.data['showcover']) == 1:
            return True
        else:
            return False

    class Meta:
        model = Article
        fields = ['title', 'cover', 'content', 'publish', 'showcover']
