import random
from time import sleep

import datetime
import os, sys
#
# sys.path.append('/new_sand/guoku/nut/nut')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_anchen'

sys.path.append('/data/www/nut')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


# #
from apps.order.models import Order



dist_source = [(9, 1),
        (10, 47),
        (11, 83),
        (12, 172),
        (13, 172),
        (14, 104),
        (15, 164),
        (16, 160),
        (17, 144),
        (18, 170),
        (19, 142),
        (20, 100),
        (21, 27),
        (23, 7)]


def make_dist(source):
    dist = []
    for item in source:
        dist += [item[0]] * item[1]
    return dist

hour_distribution = make_dist(dist_source)


def get_orders():
    seller_ids = ['2014284','2014283','2014282']
    seller_mails = ['dyseller1@guoku.com', 'dyseller2@guoku.com', 'dyseller3@guoku.com']
    seller_orders = Order.objects.filter(customer_id__in=seller_ids)
    return seller_orders

def get_date(origin_payment_time):
    pass


def create_time(date, hour, minut):
    datetime.datetime
    pass


def generate_create_time(origin_create_time):

    hour = random.choice(hour_distribution)
    minute = random.randint(1, 59)
    second = random.randint(1, 59)
    return origin_create_time.replace(hour=hour, minute=minute, second=second)


def make_minut_plus(created_datetime, time_plus):
    pass


def generate_update_time(created_datetime):
    minute_plus = random.randint(1, 15)
    second_plus = random.randint(1,59)
    return created_datetime + datetime.timedelta(minutes=minute_plus, seconds=second_plus)


def generate_order_number(order):

    key = order.created_datetime.strftime("%Y%m%d%H%M")
    count = 1
    number = "%s%s" % (key, count)
    while True:
        if Order.objects.filter(number=number).exists():
            count += 1
            number = "%s%s" % (key, count)
        else:
            return number

def adjust_single_order(order):
    print('begin adjust order number : %s' % order.number)
    print('origin time %s' % order.created_datetime)
    print('payment time %s' % order.updated_datetime)
    # print('order seller %s' % order.customer.nick)

    origin_create_time = order.created_datetime

    order.created_datetime = generate_create_time(origin_create_time)
    order.updated_datetime = generate_update_time(order.created_datetime)
    order.number = generate_order_number(order)

    print('new order number %s' % order.number)
    print('new created_datetime %s' % order.created_datetime)
    print('new updated_datetime %s' % order.updated_datetime)

    order.save()


def adjust_order_time():
    index = 0
    orders = get_orders()
    for order in orders:
        index += 1
        print('order : %s'  % index)
        adjust_single_order(order)
    print('all done. ')
    exit(0)


if __name__ == '__main__':
    print('in....')
    adjust_order_time()