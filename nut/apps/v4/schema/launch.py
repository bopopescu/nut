from marshmallow import Schema, fields, pprint


class LaunchSchema(Schema):
    launch_id           = fields.Integer(attribute="id")
    title               = fields.String()
    description         = fields.String()
    version             = fields.String()
    action_title        = fields.String()
    action              = fields.String()
    launch_image_url    = fields.URL()