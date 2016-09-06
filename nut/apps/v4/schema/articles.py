from marshmallow import Schema, fields, pprint
from apps.v4.schema.users import UserSchema

class ArticleSchema(Schema):

    article_id          = fields.Integer(attribute='id')
    creator             = fields.Nested(UserSchema, many=False)
    title               = fields.String()
    cover               = fields.String()
    content             = fields.String()
    # content             = fields.String(attribute='strip_tags_content')
    publish             = fields.Integer()
    tags                = fields.Method('get_tag_list')
    url                 = fields.Method('get_url')
    is_dig              = fields.Method('check_is_dig')

    read_count          = fields.Integer()
    comment_count       = fields.Integer(attribute='comment_count')
    digest              = fields.String(attribute='digest')
    dig_count           = fields.Integer(attribute='dig_count')

    pub_time            = fields.Method('selection_pub_time')

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_tag_list(self, obj):
        return obj.tag_list

    def selection_pub_time(self, obj):
        pub_time     = None
        try:
            pub_time = self.context['pub_time']
        except KeyError:
            pass
        return pub_time

    def check_is_dig(self, obj):
        isDig = False
        try:
            if obj.id in self.context['articles_list']:
                isDig = True
        except KeyError as e:
            pass
        return isDig



if __name__ == "__main__":
    import os, sys

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
    from apps.v4.models import APIArticle

    art = APIArticle.objects.get(pk=51954)

    article_schema = ArticleSchema(many=False)
    result = article_schema.dump(art)
    pprint(result.data, indent=2)