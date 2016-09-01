from marshmallow import Schema, fields, pprint


class UserSchema(Schema):

    user_id             = fields.Integer(attribute='id')
    email               = fields.Email(required=True)

    # user profile
    nickname            = fields.Method('get_nickname')
    nick                = fields.Method('get_nick')
    bio                 = fields.Method('get_bio')
    gender              = fields.Method('get_gender')
    location            = fields.Method('get_location')
    city                = fields.Method('get_city')
    website             = fields.Method('get_website')
    avatar_large        = fields.Method('get_avatar_url')
    avatar_small        = fields.Method('get_avatar_url')

    mail_verified       = fields.Boolean(attribute='is_verified')
    authorized_author   = fields.Integer(attribute='authorized_author')

    like_count          = fields.Integer(attribute='like_count')
    entity_note_count   = fields.Integer(attribute='post_note_count')
    tag_count           = fields.Integer(attribute='tags_count')
    dig_count           = fields.Integer(attribute='dig_count')
    fan_count           = fields.Integer(attribute='fans_count')
    following_count     = fields.Integer(attribute='following_count')


    def get_nickname(self, obj):
        return obj.profile.nickname

    def get_nick(self, obj):
        return obj.profile.nick

    def get_gender(self, obj):
        return obj.profile.gender

    def get_bio(self, obj):
        return obj.profile.bio

    def get_location(self, obj):
        return obj.profile.location

    def get_city(self, obj):
        return obj.profile.city

    def get_website(self, obj):
        return obj.profile.website

    def get_avatar_url(self, obj):
        # print self.context['visitor']
        return obj.profile.avatar_url


if __name__ == "__main__":
    import os, sys

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
    from apps.v4.models import APIUser

    u = APIUser.objects.get(pk=1)

    user_schema = UserSchema(many=True)
    user_schema.context['visitor'] = u
    result = user_schema.dump(u, many=False)
    pprint(result.data, indent=2)