from wtforms import Form, StringField, validators


class HotWordsForm(Form):

    words       = StringField('HTWords', [validators.Length(min=1, max=25)])