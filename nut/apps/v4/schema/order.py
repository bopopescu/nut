# coding=utf-8

import time
from marshmallow import Schema, fields
from apps.v4.schema.users import UserSchema



class ShippingAddressSchema(Schema):

    shipping_id         = fields.Integer(attribute="id")
    user                = fields.Nested(UserSchema, many=False)
    country             = fields.String()
    province            = fields.String()
    city                = fields.String()
    street              = fields.String()
    detail              = fields.String()
    post_code           = fields.String()
    type                = fields.Integer()
    contact_phone       = fields.String()



class OrderSchema(Schema):

    order_id            = fields.Integer(attribute='id')
    customer            = fields.Nested('UserSchema', many=False)
    number              = fields.String()
    status              = fields.Integer()
    shipping_to         = fields.Nested(ShippingAddressSchema, exclude=('user',), many=False)
    order_items         = fields.Nested('OrderItemSchema', exclude=('order', 'order_item_id'),
                                        many=True, attribute='items.all')
    order_total_value   = fields.Number(attribute='order_total_value')
    created_datetime    = fields.Method('get_created_datetime')
    updated_datetime    = fields.Method('get_updated_datetime')

    # wx_payment_qrcode_url   = fields.String(attribute='wx_payment_qrcode_url')


    def get_created_datetime(self, obj):
        return time.mktime(obj.created_datetime.timetuple())

    def get_updated_datetime(self, obj):
        return time.mktime(obj.updated_datetime.timetuple())


class OrderItemSchema(Schema):
    order_item_id       = fields.Integer(attribute='id')
    # order               = fields.Nested('OrderSchema', many=False)
    entity_title        = fields.String(attribute='item_title')
    entity_image        = fields.String(attribute='image')
    attr                = fields.Method('get_sku_attr')
    volume              = fields.Integer()
    add_time            = fields.DateTime()
    grand_total_price   = fields.Number()
    promo_total_price   = fields.Number()


    def get_sku_attr(self, obj):
        attr_string = ''

        for k, v in obj.attrs.items():
            attr_string += u"{0} / {1};".format(k, v)

        return attr_string[:-1]
        # return obj.sku.attrs



