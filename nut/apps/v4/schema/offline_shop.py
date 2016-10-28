from marshmallow import Schema, fields, pprint


class OfflineShop(Schema):

    store_id        = fields.Integer(attribute='id')
    store_name      = fields.String(attribute='shop_name')
    store_desc       = fields.String(attribute='shop_desc')
    store_link       = fields.URL(attribute='mobile_url')
    chief_image     = fields.Method('get_chief_image')
    images          = fields.Method('get_images')

    def get_images(self, obj):
        return obj.images

    def get_chief_image(self, obj):
        if len(obj.images) > 0:
            return obj.images[0]
        return ''