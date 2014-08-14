import os, sys
sys.path.append('/Users/edison/PycharmProjects/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from pymongo import MongoClient
from bson.objectid import ObjectId


from apps.core.models import Banner

client = MongoClient('mongodb://10.0.2.200:27017/')
db = client.guoku


def get_image_from_mongo(image_key):

    collection = db.image

    image =  collection.find_one({'_id':ObjectId(image_key)})
    return image['store_hash']


def update_banner_image():
    banners = Banner.objects.all()

    for banner in banners:
        # print banner.image, banner.id
        image = get_image_from_mongo(banner.image)
        image_url = "img/%s.jpg" % image
        # print image_url
        banner.image = image_url
        banner.save()

if __name__ == '__main__':
    update_banner_image()



__author__ = 'edison'
