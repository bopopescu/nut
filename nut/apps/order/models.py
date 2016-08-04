#encoding=utf-8
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.order.manager import OrderManager
from apps.order.manager.sku import SKUManager
from apps.order.manager.cart import CartItemManager
from apps.core.extend.fields.listfield import ListObjectField

from apps.payment.alipay import AliPayPayment

class SKU(models.Model):
    (disable, enable) =  (0, 1)
    SKU_STATUS_CHOICE = [(disable, _('disable')), (enable, _('enable'))]
    entity = models.ForeignKey('core.Entity', related_name='skus')
    attrs = ListObjectField()
    stock = models.IntegerField(default=0,db_index=True)#库存
    origin_price = models.FloatField(default=0, db_index=True)
    promo_price = models.FloatField(default=0, db_index=True)
    status =  models.IntegerField(choices=SKU_STATUS_CHOICE, default=enable)
    objects =  SKUManager()


    @property
    def attrs_json_str(self):
        return json.dumps(self.attrs)

    @property
    def attrs_display(self):
        attr_str_list = list()
        for key , value in self.attrs.iteritems():
            attr_str_list.append('%s:%s'%(key,value))
        return '/'.join(attr_str_list)

    # class Meta:
    #     #TODO : unique together didn't work
    #     unique_together = ('entity' ,'attrs')


class CartItem(models.Model):
    user = models.ForeignKey('core.GKUser', related_name='cart_items',db_index=True)
    sku  = models.ForeignKey(SKU, db_index=True)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True,db_index=True)

    objects =CartItemManager()

    class Meta:
        ordering = ['-add_time']

    def generate_order_item(self, order):
        order_item, created = OrderItem.objects.get_or_create(
            order=order, sku=self.sku , customer=order.customer,
            defaults={
                'grand_total_price': self.grand_total_price,
                'promo_total_price' : self.promo_total_price
            }
        )
        if created:
            order_item.volume = self.volume
            order_item.save()
        return  order_item


    @property
    def grand_total_price(self):
        return self.sku.origin_price * self.volume

    @property
    def promo_total_price(self):
        return self.sku.promo_price * self.volume

    @property
    def shipping_cost(self):
        raise NotImplemented()
        return 0



class ShippingAddress(models.Model):
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


class Order(models.Model):

    (   address_unbind, #
        waiting_for_payment,#未付款
            paid, #已经付款,出库中
            send, #货物在途,
            closed, #已经签收
            refund_submit, #收到退款申请
            refund_sku_got, #处理货品回收
            refund_done, #货款已经退回
            ) = range(1,9)

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

    customer = models.ForeignKey('core.GKUser', related_name='orders')
    number = models.CharField(max_length=128, db_index=True, unique=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICE, default=address_unbind)
    shipping_to  = models.ForeignKey(ShippingAddress, null=True, blank=True)

    objects = OrderManager()

    def generate_alipay_payment_url(self, host='http://www.guoku.com'):
        return AliPayPayment(order=self,host=host).payment_url

    def generate_weixin_payment_url(self,host='http://www.guoku.com'):
        return

    def set_paid(self):
        self.status = Order.paid
        self.save()
        return self

    def set_closed(self):
        self.status = Order.closed
        self.save()
        return self

    @property
    def payment_subject(self):
        #TODO : need define more prise subject
        return 'GUOKU Order :%s' %self.number
        # raise  NotImplemented()

    @property
    def payment_body(self):
        items = map(lambda item:item.title , self.items.all())
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
        return reduce(lambda a,b : a + b,
                        [item.promo_total_price for item in self.items.all()])

    @property
    def grand_total_price(self):
        return reduce(lambda a,b : a+b ,
                        [item.grand_total_price for item in self.items.all()])

    @property
    def order_total_value(self):
        return self.promo_total_price + self.shipping_fee

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items')
    customer = models.ForeignKey('core.GKUser', related_name='order_items',db_index=True)
    sku = models.ForeignKey(SKU, db_index=True)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True,db_index=True)
    grand_total_price = models.FloatField(null=False) # 当订单生成的时候计算
    promo_total_price = models.FloatField(null=False) # 当订单生成的时候计算

    @property
    def title(self):
        return self.sku.entity.title


class OrderMessage(models.Model):
    '''
        订单意见纪录,可以由用户填写,也可以由客服填写
    '''
    order = models.ForeignKey(Order)
    user = models.ForeignKey('core.GKUser')
    message = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)









