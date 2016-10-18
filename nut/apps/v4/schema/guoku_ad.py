from marshmallow import Schema, fields

class GKADSchema(Schema):
    id              = fields.Integer()
    image_url       = fields.URL()
    click_url       = fields.URL(attribute='url')
