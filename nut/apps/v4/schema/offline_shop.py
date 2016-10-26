from marshmallow import Schema, fields, pprint


class OfflineShop(Schema):

    shop_name       = fields.String()
    shop_desc       = fields.String()
    shop_link       = fields.URL(attribute='mobile_url')
    # images          = fields.List()
    chief_image     = fields.String(attribute='chief_image')
    images          = fields.Method()

    def get_images(self, obj):
        return obj.images

    def get_chief_image(self, obj):
        if len(obj.images) > 0:
            return obj.images[0]
        return ''