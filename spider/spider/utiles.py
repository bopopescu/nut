#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'judy'

from money import XMoney

import urllib2
import json


def currency_converting(convert_from, amount, convert_to='CNY'):
    """ Currency converting.
    Used Yahoo currency API.

    Args:
        convert_from: A three-letter currency code.
        amount: The amount want to convert. Can be any valid value for decimal
                or integer.
        convert_to: Default CNY. A three-letter currency code.

    Returns:
        A decimal.
    """
    #TODO(Judy): save the rate to Redis.

    yql_query_url = "https://query.yahooapis.com/v1/public/yql?q=" \
                    "select%20*%20from%20yahoo.finance.xchange%20where" \
                    "%20pair%20in%20(%22" + convert_from + "%22%2C%20%22" + \
                    convert_to + "%22)&format=json&env=store%3A%2F%2" \
                    "Fdatatables.org%2Falltableswithkeys&callback="
    try:
        yql_response = urllib2.urlopen(yql_query_url)
        try:
            yql_json = json.loads(yql_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON format error"
        currency_output = amount * float(
            yql_json['query']['results']['rate'][-1]['Rate'])
        return round(currency_output, 2)

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason
