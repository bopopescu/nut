import os, sys
sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from pymongo import MongoClient
from bson.objectid import ObjectId

from django.conf import settings
client = MongoClient('mongodb://10.0.2.200:27017/')
db = client.guoku
collection = db.image

image_host = getattr(settings, 'IMAGE_HOST', None)


from apps.core.models import Entity

def get_image_from_mongo(image_key):
    image =  collection.find_one({'_id':ObjectId(image_key)})
    url = None
    try:
        url =  image['origin_url']
    except KeyError:
        hash_value = image.get('store_hash', None)
        if hash:
            url = "%simg/%s.jpg" % (image_host, hash_value)

    return url

# e = Entity.objects.all()
import MySQLdb
import MySQLdb.cursors

db = MySQLdb.connect(host='10.0.2.90',
                   user='qinzhoukan',
                   passwd='qinzhoukan1@#',
                   db='guoku',
                   cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

cursor.execute("SELECT id, chief_image, detail_images FROM base_entity ORDER BY id  DESC")
for row in cursor.fetchall():
    print row['id']
    if len(row['chief_image']) == 0:
        continue

    images = []
    try:
        image = get_image_from_mongo(row['chief_image'])
        images.append(image)


        detail_images = row['detail_images']
        if len(detail_images) > 0:
            detail_images = detail_images.split('#')
            # print detail_images

            for i in detail_images:
                if len(i) == 0:
                    continue
                print i
                image = get_image_from_mongo(i)
                if image is None:
                    continue
                images.append(image)
            print images

        # print image
        entity = Entity.objects.get(pk = row['id'])
        entity.images = images
        entity.save()
        # print entity
    except Entity.DoesNotExist, e:
        print e.message
__author__ = 'edison'
