from apps.core.forms.user import UserForm


class UserSettingsForm(UserForm):

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserSettingsForm, self).__init__(*args, **kwargs)


    def save(self):

        pass

__author__ = 'edison'
