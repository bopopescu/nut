from django import forms


class TaobaoForm(forms.Form):

    taobao_id = forms.CharField(
        widget=forms.TextInput()
    )

    taobao_token = forms.CharField(
        widget=forms.TextInput()
    )

    screen_name = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )

__author__ = 'edison'
