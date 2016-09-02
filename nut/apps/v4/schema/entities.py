from marshmallow import Schema, fields


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
    detail_images       = fields.String(attribute='detail_images')
    price               = fields.Number()

    like_count          = fields.Integer(attribute='like_count')
    note_count          = fields.Integer(attribute='note_count')
    like_already        = fields.Method('get_like_already')

    # buy_links           = fields.Nested(BuyLinkSchema, exclude=('id',), attribute='buy_links.all', many=True)

    def get_like_already(self, obj):
        like_already = 0
        if obj.id in self.context['user_like_list']:
            like_already = 1

        return like_already


