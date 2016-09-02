import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from pprint import pprint
# from apps.v4.models import APIUser
# from apps.v4.schema.users import UserSchema
#
#
# u = APIUser.objects.get(pk=1)
#
# user_schema = UserSchema(many=True)
# user_schema.context['visitor'] = u
# result = user_schema.dump(u, many=False)
# pprint(result.data, indent=2)


from apps.core.models import Entity
from apps.v4.schema.entities import EntitySchema

entity_schema = EntitySchema(many=False)
e = Entity.objects.all().last()

# print e.buy_links.all()
pprint(entity_schema.dump(e).data , indent=2)
