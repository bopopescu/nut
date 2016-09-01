from marshmallow import Schema, fields
from apps.v4.schema.users import UserSchema


class ShippingAddressSchema(Schema):

    shipping_id         = fields.Integer(attribute="id")
    user                = fields.Nested(UserSchema, many=False)


class OrderSchema(Schema):

    order_id            = fields.Integer(attribute='id')
    customer            = fields.Nested(UserSchema, many=False)
    number              = fields.String()
    status              = fields.Integer()
    shipping_to         = fields.Nested(ShippingAddressSchema, exclude=('user',), many=False)

    created_datetime    = fields.DateTime()
    updated_datetime    = fields.DateTime()


class OrderItemSchema(Schema):
    order_item_id       = fields.Integer(attribute='id')
    order               = fields.Nested(OrderSchema, many=False)
    volume              = fields.Integer()
    add_time            = fields.DateTime()
    grand_total_price   = fields.Number()
    promo_total_price   = fields.Number()

