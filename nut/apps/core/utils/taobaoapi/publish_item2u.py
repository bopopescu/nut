# -*- coding: utf-8 -*-
from top.api import SpContentItemPublishRequest, SpContentItemUpdateRequest
from top import appinfo
# from django.utils.log import getLogger
# #
# #
# log = getLogger('django')

class PublishItem2U():

    def __init__(self, app_key, app_secret):
        self.req = SpContentItemPublishRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))
        self.req.site_key = '7z2z61l918d7k80592e46154dl321fk6'

    def publish(self, **kwargs):
        # print kwargs
        title = kwargs.pop('title', None)
        comments = kwargs.pop('comments', None)

        self.req.item_id = kwargs.pop('item_id', None)
        self.req.title = title
        self.req.comments = comments
        self.req.detailurl = kwargs.pop('detailurl', None)
        self.req.classname = kwargs.pop('category', None)
        self.req.tags = u"新有好货"
        # print self.req.title
        # print self.req.comments
        resp = {}
        try:
            resp = self.req.getResponse()

        except Exception, e:
            print e
            # log.error(e.message)
        finally:
            return resp


class UpdateItem2U():

    def __init__(self, app_key, app_secret):
        self.req = SpContentItemUpdateRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))
        self.req.site_key = '7z2z61l918d7k80592e46154dl321fk6'

    def update(self, **kwargs):
        title = kwargs.pop('title', None)
        comments = kwargs.pop('comments', None)

        self.req.id = kwargs.pop('id', None)
        self.req.item_id = kwargs.pop('item_id', None)
        self.req.title = title
        self.req.comments = comments
        self.req.detailurl = kwargs.pop('detailurl', None)
        self.req.classname = kwargs.pop('category', None)
        self.req.tags = u"新有好货,果库新品"

        resp = {}
        try:
            resp = self.req.getResponse()
        except Exception, e:
            print e.message
            # log.error(e.message)
        finally:
            return resp



if __name__=="__main__":

    u = PublishItem2U(app_key='23198909', app_secret='cc35120d1fb84446300eb1092fae4abe')

    resp = u.publish(
        item_id = '14329051759',
        title='test',
        comments='test',
        # detailurl='http://www.guoku.com/detail/c7fb6489/',
        detailurl='http://guoku.uz.taobao.com/detail/e92780d8/'
    )

    uid = resp['sp_content_item_publish_response']['value']

    # p = UpdateItem2U(app_key='23198909', app_secret='cc35120d1fb84446300eb1092fae4abe')
    #
    # resp = p.update(
    #     id = uid,
    #     item_id = '39502923104',
    #     title='test',
    #     comments='test',
    #     # detailurl='http://www.guoku.com/detail/c7fb6489/',
    #     detailurl='http://guoku.uz.taobao.com/detail/%s/' % uid
    # )

    print resp

__author__ = 'edison'
