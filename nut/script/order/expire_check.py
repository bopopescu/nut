import os, sys

# sys.path.append('/data/www/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


sys.path.append('/new_sand/guoku/nut/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'


from apps.order.models import Order


orders = Order.objects.filter(status__in=[Order.address_unbind, Order.waiting_for_payment])
for order in orders:
    if order.should_expired:
        order.set_expire()
#