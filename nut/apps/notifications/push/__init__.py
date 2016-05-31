#coding=utf-8

import jpush
from django.conf import settings
from django.utils.log import getLogger


app_key = getattr(settings, 'JPUSH_KEY', None)
app_secret = getattr(settings, 'JPUSH_SECRET', None)

log = getLogger('django')

class PushException(Exception):
    pass


class PushMessageBase(object):
    def __init__(self, sender, instance, created, **kwargs):
        self._instance = instance
        self._sender = sender
        self._created = created
        self._kwargs =  kwargs
        self._jpush = jpush.JPush(app_key, app_secret)
        try :
            self.send_message(self.create_message())
        except  PushException as e:
            log.error('push message exeption for instance %s' %instance)


    def create_message(self):
        msg_dic = self.get_message_dic()
        ios_msg = jpush.ios(**msg_dic)
        msg_dic.pop('badge', None)
        android_msg = jpush.android(**msg_dic)
        push = self._jpush.create_push()
        push.notification = jpush.notification(
                        alert=self.get_verb().encode('utf8'),
                        ios=ios_msg,
                        android=android_msg)
        push.platform = jpush.all_
        push.options =  {"time_to_live":86400,
                         "apns_production":True}
        return push

    def get_message_dic(self):
        msg_dic =  {
            'alert' : self.get_verb().encode('utf8'),
            'badge' :self.get_badge(),
            'extras': self.get_extra()
        }
        return  msg_dic

    def get_verb(self):
        raise NotImplemented()

    def get_extra(self):
        raise NotImplemented()

    def get_badge(self):
        return self._instance.recipient.notifications.unread().count()


    def get_receivers(self):
        return [reg.rid for reg in self._instance.recipient.jpush_token.all()]

    def send_message(self,message):
        for rid in self.get_receivers():
            message.audience = jpush.registration_id(rid)
            try:
                message.send()
            except jpush.JPushFailure as e :
                raise PushException()


class FollowMessage(PushMessageBase):
    def get_verb(self):
        return  self._instance.actor.profile.nick + u' 开始关注你'

    def get_extra(self):
        return {'url':'guoku://user/%s' % self._instance.actor.pk}


class SelectionEntityMessage(PushMessageBase):
    def get_verb(self):
        return u' 你添加的商品被收入精选'

    def get_extra(self):
        return {'url': 'guoku://entity/%s' % self._instance.target.pk}


class NoteMessage(PushMessageBase):
    def get_verb(self):
        return self._instance.actor.profile.nick + u' 点评了你推荐的商品'

    def get_extra(self):
        return {'url': 'guoku://entity/%s' % self._instance.target.pk}


class PokeMessage(PushMessageBase):
    def get_verb(self):
        return self._instance.actor.profile.nick + u' 赞了你撰写的点评'

    def get_extra(self):
        return {'url': 'guoku://entity/%s' % self._instance.target.entity.pk}


msg_table = {
            'user_follow': FollowMessage,
            'selection_entity': SelectionEntityMessage,
            'note': NoteMessage,
            'note_poke': PokeMessage
        }


class PushMessageBase(object):
    def get_audience(self):
        pass
    def get_message_dic(self):
        pass
    def send_message(self):
        pass
    def create_message(self):
        pass

class JPushMessageBase(PushMessageBase):
    def __init__(self):
        self._jpush = jpush.JPush(app_key, app_secret)
        self.push = self._jpush.create_push()
    pass

class TestPushMessage(JPushMessageBase):
    def __init__(self,rid, message, url):
        self._rid = rid
        self._message = message
        self.url = url
        super(TestPushMessage, self).__init__()

    def get_message_dic(self):
        return {
            'alert': self._message,
            'extras':{
                'url':self._url
            }
        }

    def create_message(self):
        msg_dic = self.get_message_dic()
        ios_msg = jpush.ios(**msg_dic)
        msg_dic.pop('badge', None)
        android_msg = jpush.android(**msg_dic)
        push = self._push
        push.notification = jpush.notification(
                        alert=self._message,
                        ios=ios_msg,
                        android=android_msg)
        push.platform = jpush.all_
        push.options =  {"time_to_live":86400,
                         "apns_production":True}

    def get_audience(self):
        return None

    def send_message(self):
        self.push.audience  = jpush.registration_id('0815c850d66')
        self._push.send()






class MessageFactroy(object):
    def __init__(self):
        pass

    def create_test_message(self):

        pass

    def create_notify_message(self, sender, instance, created, **kwargs):
        action_model_name = instance.action_object_content_type.model
        if action_model_name in msg_table:
            return msg_table[action_model_name](sender,instance, created, **kwargs)
        else :
            # log.info('message type not supportted!')
            pass

