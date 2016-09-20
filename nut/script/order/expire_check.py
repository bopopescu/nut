import os, sys

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


from apps.order.models import Order


orders = Order.objects.filter(status_in=[Order.address_unbind, Order.waiting_for_payment])
for order in orders:
    if order.should_expired:
        order.set_expire()
#