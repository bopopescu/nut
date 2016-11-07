import time
from marshmallow import Schema, fields
from apps.v4.schema.users import UserSchema


class BuyLinkSchema(Schema):

    id                  = fields.Integer()
    shop_nick           = fields.String()
    buy_link            = fields.String()
    price               = fields.Number()
    volume              = fields.Integer()


class EntitySchema(Schema):

    entity_id           = fields.Integer(attribute='id')
    entity_hash         = fields.String()

    brand               = fields.String()
    title               = fields.String()

    chief_image         = fields.String(attribute='chief_image')
    detail_images       = fields.Method('get_detail_images')
    price               = fields.Number()
    status              = fields.Boolean()

    like_count          = fields.Integer(attribute='like_count')
    note_count          = fields.Integer(attribute='note_count')
    like_already        = fields.Method('get_like_already')

    # buy_links           = fields.Nested(BuyLinkSchema, exclude=('id',), attribute='buy_links.all', many=True)

    def get_detail_images(self, obj):
        return obj.detail_images

    def get_like_already(self, obj):
        like_already = 0
        if not self.context.has_key('user_like_list'):
            return like_already

        if obj.id in self.context['user_like_list']:
            like_already = 1

        return like_already


class EntityNoteSchema(Schema):

    note_id             = fields.Integer(attribute='id')
    content             = fields.Integer(attribute='note')
    comment_count       = fields.Integer(attribute='comment_count')
    poke_count          = fields.Integer(attribute='poke_count')
    created_time        = fields.Method('get_created_time')
    updated_time        = fields.Method('get_updated_time')
    creator             = fields.Nested('UserSchema', exclude=('user_id',), uselist=False)

    def get_created_time(self, obj):
        return time.mktime(obj.post_time.timetuple())

    def get_updated_time(self, obj):
        return time.mktime(obj.updated_time.timetuple())