from pprint import pprint
from django.db import models
from django.utils.log import getLogger

from apps.order.exceptions import CartException, OrderException

log = getLogger('django')


class CartItemQueryset(models.query.QuerySet):
    pass

class CartItemManager(models.Manager):

    def cart_item_count_by_user(self, user):
        return self.get_queryset().filter(user=user).count()

    def add_sku_to_user_cart(self, user, sku, volume=1):
        if self.cart_item_count_by_user(user) > 1000 :
            raise CartException('too many item in cart ')

        if sku.status == 0 or sku.stock <= 0:
            raise CartException('sku out of stock , can not be added to cart')

        if sku.stock < volume:
            raise CartException('sku stock less than required')

        cart_item, created =  self.get_or_create(sku=sku, user=user)
        if created:
            cart_item.volume = volume
            cart_item.save()
        else :
            cart_item.volume += volume
            cart_item.save()
        return cart_item

    def remove_sku_from_user_cart(self, user, sku):
        try:
            cart_item = self.get(user=user,sku=sku)
            cart_item.delete()
        except models.Model.DoesNotExist as e :
            return
        except models.Model.MultipleObjectsReturned as e :
            self.filter(user=user, sku=sku).delete()
            return


    def decr_sku_in_user_cart(self, user, sku):
        try:
            cart_item = self.get(user=user, sku=sku)
            cart_item.volume -= 1
            if cart_item.volume <= 0 :
                self.remove_sku_from_user_cart(user, sku)
            else :
                cart_item.save()
                return cart_item

        except models.Model.DoesNotExist as e :
            return None

        except models.Model.MultipleObjectsReturned as e :
            cart_items = self.filter(user=user, sku=sku)
            cart_items[0].volume -= 1
            cart_items[0].save()
            for citem in cart_items[1:]:
                citem.delete()
            return cart_items[0]


    def clear_user_cart(self, user):
        self.filter(user=user).delete()


    # some circular reference problem

    # def checkout_user_cart(self, user):
    #     new_order = None
    #     if self.cart_item_count <= 0 :
    #         raise CartException('cart is empty')
    #     else :
    #         try :
    #             new_order = Order.objects.create(**{
    #                 'customer': self,
    #                 'number': Order.objects.generate_order_number()
    #
    #             })
    #             for cart_item in self.cart_items.all():
    #                 order_item = None
    #                 try :
    #                     order_item = cart_item.generate_order_item(new_order)
    #                 except Exception as e:
    #                     log.error('create_order item error :%s'%e)
    #                     if order_item:
    #                         order_item.delete()
    #                     raise OrderException('error when create order item')
    #             self.clear_cart()
    #             return new_order
    #
    #         except Exception as e :
    #             # if exception happens
    #             pprint(e)
    #             log.error(e)
    #             if new_order:
    #                 new_order.delete()
    #             # raise OrderException('error create order')
    #             return None
