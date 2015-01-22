from django import forms

class WeiboForm(forms.Form):

    sina_id = forms.CharField(
        widget=forms.TextInput()
    )

    sina_token = forms.CharField(
        widget=forms.TextInput()
    )

    screen_name = forms.CharField(
        widget=forms.TextInput()
    )

__author__ = 'edison'
