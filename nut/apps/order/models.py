#encoding=utf-8
import json

from datetime import timedelta, datetime
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.db.models import PROTECT
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger

from apps.core.base import BaseModel
from apps.order.manager import OrderManager
from apps.order.manager.sku import SKUManager
from apps.order.manager.cart import CartItemManager
from apps.core.extend.fields.listfield import ListObjectField
# from apps.core.models import BaseModel

from apps.payment.alipay import AliPayPayment
from apps.payment.weixinpay import WXPayment
from apps.order.exceptions import OrderException, CartException

log = getLogger('django')


class SKU(BaseModel):
    (disable, enable) = (0, 1)
    SKU_STATUS_CHOICE = [(disable, _('disable')), (enable, _('enable'))]
    entity = models.ForeignKey('core.Entity', related_name='skus')
    attrs = ListObjectField()
    stock = models.IntegerField(default=0,db_index=True)#库存
    origin_price = models.FloatField(default=0, db_index=True)
    discount = models.FloatField(default=1, db_index=True)
    promo_price = models.FloatField(default=0, db_index=True)
    status = models.IntegerField(choices=SKU_STATUS_CHOICE, default=enable)
    objects = SKUManager()

    class Meta:
        ordering = ['-stock']

    def get_discount_rate(self):
        if self.origin_price == 0  or self.promo_price == 0 :
            return 1
        return self.promo_price/(self.origin_price*1.0)


    @property
    def attrs_json_str(self):
        return json.dumps(self.attrs)

    @property
    def attrs_display(self):
        attr_str_list = list()
        for key , value in self.attrs.iteritems():
            attr_str_list.append('%s:%s' % (key, value))
        return '/'.join(attr_str_list)

    def save(self, *args, **kwargs):
        self.discount = self.get_discount_rate()
        self.entity.updated_time = datetime.now()
        self.entity.save()
        super(SKU, self).save(*args, **kwargs)

    # def toDict(self):
    #     res = super(SKU, self).toDict()
    #     res.pop('attrs', None)
    #     res['attrs'] = getattr(self, 'attrs')
    #     return res


    # class Meta:
    #     #TODO : unique together didn't work
    #     unique_together = ('entity' ,'attrs')


class CartItem(BaseModel):
    user = models.ForeignKey('core.GKUser', related_name='cart_items',db_index=True)
    # when delete sku , CartItem will be deleted
    # this is django's default action
    # in OrderItem , use PROTECT to prevent sku be deleted.
    sku = models.ForeignKey(SKU, db_index=True)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True,db_index=True)

    objects = CartItemManager()

    class Meta:
        ordering = ['-add_time']

    def generate_order_item(self, order):
        if self.sku.stock < self.volume:
            raise OrderException('sku no longer enough')
        order_item, created = OrderItem.objects.get_or_create(
            order=order, sku=self.sku, customer=order.customer,
            defaults={
                'grand_total_price': self.grand_total_price,
                'promo_total_price': self.promo_total_price
            }
        )
        if created:
            order_item.volume = self.volume
            order_item.item_title = self.sku.entity.title
            order_item.image = self.sku.entity.chief_image
            order_item.attrs = self.sku.attrs
            order_item.entity_link = self.sku.entity.absolute_url
            order_item.save()
        return order_item


    @property
    def grand_total_price(self):
        return self.sku.origin_price * self.volume

    @property
    def promo_total_price(self):
        return self.sku.promo_price * self.volume

    @property
    def shipping_cost(self):
        raise NotImplemented()
        # return 0


class ShippingAddress(BaseModel):
    (normal, special) = range(1,3)
    SHIPPINGADDRESS_TYPE_CHOICE = (
        (normal,_('normal address')),
        (special,_('special address'))
    )
    user = models.ForeignKey('core.GKUser', related_name='shipping_addresses')
    country = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=128)
    detail = models.CharField(max_length=128)
    post_code = models.CharField(max_length=32)
    type = models.IntegerField(choices=SHIPPINGADDRESS_TYPE_CHOICE, default=normal)
    contact_phone = models.CharField(max_length=64)


    def _cal_shipping_fee(self):
        raise NotImplemented()

    @property
    def shipping_fee(self):
        if self.type == self.special:
            return 0
        else :
            return self._cal_shipping_fee()


class Order(BaseModel):
    expire_in_minutes = 60

    (   expired, #超时订单,失效订单
        address_unbind, #需要客户地址  , deprecate ,
        # TODO , remove address_unbind status ,
        waiting_for_payment,#未付款
        paid, #已经付款,出库中
        send, #货物在途,
        closed, #已经签收 , tobe changed

        # TODO , change this to finished ,
        # TODO , closed will be used for abnormally finished order
        #        1.  order is expired , then order status will be set closed
        #        2.  order is closed by user ,
        #        'closed' status will be set as order is for some reason close abnormally

        refund_submit, #收到退款申请
        refund_sku_got, #处理货品回收
        refund_done, #货款已经退回
    ) = range(0, 9)

    ORDER_STATUS_CHOICE = [
        (address_unbind, _('address unbind')),
        (waiting_for_payment, _('waiting for payment')),
        (paid, _('order paid')),
        (send, _('order send')),
        (closed, _('order closed')),
        (refund_submit,_('refund processing')),
        (refund_sku_got,_('refund product recieved')),
        (refund_done,_('refund down')),
    ]

    # status transition table , prepare for a real state machine
    STATE_TRANSFORM_TABLE = [
        # expired order can not transfer to other status
        (expired, []),
        # address_unbind order can transfer to expired, waiting_for_payment, paid,
        (address_unbind, [expired, waiting_for_payment, paid]),
        (waiting_for_payment, [expired, address_unbind, paid]),
        (paid, [send, closed, refund_submit, refund_sku_got, refund_done]),
        (closed, [refund_submit]),
        (refund_submit, [refund_sku_got]),
        (refund_sku_got, [refund_done]),
    ]

    customer = models.ForeignKey('core.GKUser', related_name='orders')
    number = models.CharField(max_length=128, db_index=True, unique=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICE, default=waiting_for_payment)
    shipping_to = models.ForeignKey(ShippingAddress, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "<order number; {0}>".format(self.number)

    objects = OrderManager()

    class Meta:
        ordering = ['-updated_datetime', '-created_datetime']

    def generate_alipay_payment_url(self):
        return AliPayPayment(order=self).payment_url

    @property
    def realtime_status(self):
        # a wrapper around status field
        # a lot effort and complexity is on the expire status
        # TODO : need refactor.
        if self.should_expired:
            return Order.expired
        else:
            return self.status

    @property
    def alipay_qrcode_frame_page_url(self):
        # use to jump from guoku to alipay , iframe already implemented
        return reverse_lazy('web_user_order_alipay_qrcode', args=[self.id])

    @property
    def mini_alipay_qrcode_page_url(self):
        # direct to alipay , need put this url into a <iframe>
        return AliPayPayment(order=self).mini_qrcode_page_url

    def generate_weixin_payment_url(self,):
        return reverse('web_wx_payment_page', args=[self.id])

    @property
    def should_expired(self):
        expired_time = self.created_datetime + timedelta(minutes=Order.expire_in_minutes)
        return self.status < Order.paid and datetime.now() > expired_time

    @property
    def is_paid(self):
        if self.status >= Order.paid:
            return True
        else:
            return False

    @property
    def wx_prepay_id(self):
        if self.is_paid:
            return 'order_paid'
        wxpay =WXPayment(self)
        prepay_id = wxpay.get_prepay_id()
        if prepay_id == 'order_paid':
            self.set_paid()
        return prepay_id

    @property
    def wx_payment_qrcode_url(self):
        # 订单已经支付成功的情况下, 返回 'order_paid'
        if self.is_paid:
            return 'order_paid'

        wxpay = WXPayment(self)
        url =  wxpay.get_payment_qrcode_url()
        if url == 'order_paid':
            self.set_paid()
        return url

    # def update_sku_stock(self):
    #     for item in self.items.all():
    #         item.sku.stock -= item.volume
    #         item.sku.save()

    @property
    def can_set_paid(self):
        return self.status >= Order.address_unbind and not self.should_expired

    def set_paid(self):
        if not self.can_set_paid:
            raise OrderException('can not set paid')
        if self.status < self.paid:
            self.status = Order.paid
            self.save()
            return self
        elif self.status == self.paid:
            return self
        else:
            #all status greater than paid is not effected
            return self

    def set_closed(self):
        #all status greater than paid is not effected
        if self.status > Order.closed:
            return self
        if self.status >= Order.paid:
            self.status = Order.closed
            self.save()
            return self
        else:
            raise OrderException('unpaid order can not be closed')
            return self

    def _restore_sku_stock(self):
        # only can be called from  set_expired method
        # TODO : enforce last sentence
        for item in self.items.all():
            item.sku.stock += item.volume
            item.sku.save()

    def reduce_sku_stock(self):
        for item in self.items.all():
            item.sku.stock -= item.volume
            item.sku.save()

    def set_expire(self):
        if not self.should_expired:
            raise OrderException(_('order can not be set expire'))
        self.status = Order.expired
        self._restore_sku_stock()
        self.save()

    @property
    def payment_subject(self):
        #TODO : need define more prise subject
        return 'GUOKU Order :%s' % self.number
        # raise  NotImplemented()

    @property
    def payment_body(self):
        items = map(lambda item:item.title, self.items.all())
        return '\r\n'.join(items)


    @property
    def shipping_fee(self):
        '''
        calculate shipping fee for entire order for specific address(shipping_to)
        :return:
        '''
        # raise NotImplemented()
        return 0

    @property
    def promo_total_price(self):
        # promo price , without shipping fee
        return reduce(lambda a,b : a + b,
                        [item.promo_total_price for item in self.items.all()])

    @property
    def grand_total_price(self):
        # origin price , not actual price
        return reduce(lambda a,b : a+b ,
                        [item.grand_total_price for item in self.items.all()])

    @property
    def order_total_value(self):
        # final price customer need to paid
        return self.promo_total_price + self.shipping_fee

    @property
    def payment_source(self):
        if self.payments.count():
            return self.payments.all()[0].payment_source
        else:
            return None


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='items')
    customer = models.ForeignKey('core.GKUser', related_name='order_items', db_index=True)
    # use PROTECT to prevent OrderItem and SKU deletion ,
    # when user has already checkout the order
    sku = models.ForeignKey(SKU, db_index=True, on_delete=PROTECT)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)
    grand_total_price = models.FloatField(null=False)
    # 当订单生成的时候计算

    promo_total_price = models.FloatField(null=False)
    # 当订单生成的时候计算

    item_title = models.CharField(max_length=128, null=False)
    # 订单生成的时候 赋值

    image = models.CharField(max_length=256, null=False)
    # 订单生成的时候 赋值

    entity_link = models.CharField(max_length=256, null=False)
    # 订单生成的时候 赋值

    attrs = ListObjectField()

    @property
    def attrs_json_str(self):
        return json.dumps(self.attrs)

    @property
    def attrs_display(self):
        attr_str_list = list()
        for key, value in self.attrs.iteritems():
            attr_str_list.append('%s:%s' % (key, value))
        return '/'.join(attr_str_list)

    # def __unicode__(self):
    #     return self.sku.attrs_json_str

    @property
    def title(self):
        return self.item_title

    @property
    def sku_unit_grand_price(self):
        return self.grand_total_price/(1.0*self.volume)

    @property
    def sku_unit_promo_price(self):
        return self.promo_total_price/(1.0*self.volume)

    class Meta:
        ordering = ['-add_time']


class OrderMessage(BaseModel):
    '''
        订单意见纪录,可以由用户填写,也可以由客服填写
    '''
    order = models.ForeignKey(Order)
    user = models.ForeignKey('core.GKUser')
    message = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)









