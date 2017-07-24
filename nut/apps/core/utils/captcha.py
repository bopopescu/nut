# coding=utf-8
import random

from six import text_type


def to_chinese_char(digit):
    relation = list(u'零一二三四五六七八九')
    return u''.join(relation[int(i)] for i in str(digit))


def to_chinese_operator(operator):
    relation = {u'+': u'加', u'-': u'减', u'*': u'乘'}
    return relation[operator]


def chinese_math_challenge():
    operators = (u'+', u'*',)

    payload = {
        'a': random.randint(1, 9),
        'b': random.randint(1, 9),
        'operator': random.choice(operators)
    }

    if payload['a'] < payload['b'] and '-' == payload['operator']:
        payload['a'], payload['b'] = payload['b'], payload['a']

    payload['chinese_a'] = to_chinese_char(payload['a'])
    payload['chinese_b'] = to_chinese_char(payload['b'])
    payload['chinese_operator'] = to_chinese_operator(payload['operator'])

    value = eval('{a}{operator}{b}'.format(**payload))
    challenge = u'{chinese_a}{chinese_operator}{chinese_b}等于几'.format(**payload)

    return text_type(challenge), text_type(value)
