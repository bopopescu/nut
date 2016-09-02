from marshmallow import Schema, fields
from apps.core.models import Sina_Token, WeChat_Token, Taobao_Token

from django.utils.log import getLogger

log = getLogger('django')


class UserSchema(Schema):

    user_id             = fields.Integer(attribute='id')
    email               = fields.Email(required=True)

    is_active           = fields.Integer()

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
    authorized_author   = fields.Integer(attribute='is_authorized_author')
    authorized_seller   = fields.Integer(attribute='is_authorized_seller')

    like_count          = fields.Integer(attribute='like_count')
    entity_note_count   = fields.Integer(attribute='post_note_count')
    tag_count           = fields.Integer(attribute='tags_count')
    dig_count           = fields.Integer(attribute='dig_count')
    fan_count           = fields.Integer(attribute='fans_count')
    following_count     = fields.Integer(attribute='following_count')
    article_count       = fields.Integer(attribute='published_article_count')

    relation            = fields.Method('get_relation')

    sina_screen_name    = fields.Method('get_weibo_screen_name', default=None)
    taobao_nick         = fields.Method('get_taobao_nick', default=None)
    wechat_nick         = fields.Method('get_wechat_nickname', default=None)

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
        return obj.profile.avatar_url

    def get_relation(self, obj):
        relation = 0
        try:
            visitor = self.context['visitor']
            if obj.id == visitor.id:
                relation = 4
            elif obj.id in visitor.concren:
                relation = 3
            elif obj.id in visitor.following_list:
                relation = 1
            elif obj.id in visitor.fans_list:
                relation = 2
        except KeyError as e:
            pass
        return relation

    def get_weibo_screen_name(self, obj):
        screen_name = None
        try:
             screen_name = obj.weibo.screen_name
        except Sina_Token.DoesNotExist as e:
            log.info("info: %s" % e.message)
        return screen_name

    def get_taobao_nick(self, obj):
        taobao_nick = None
        try:
            taobao_nick = obj.taobao.screen_name
            # res['taobao_token_expires_in'] = self.taobao.expires_in
        except Taobao_Token.DoesNotExist as e:
            log.info("info: %s", e.message)
        return taobao_nick

    def get_wechat_nickname(self, obj):
        wecaht_nick = None
        try:
            wecaht_nick = obj.weixin.nickname
        except WeChat_Token.DoesNotExist as e:
            log.info("info: %s", e.message)
        return wecaht_nick


