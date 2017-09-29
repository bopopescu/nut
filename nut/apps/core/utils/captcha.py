# coding=utf-8
import random

from six import text_type


def to_chinese_char(digit):
    relation_lower = list(u'零一二三四五六七八九')
    relation_upper = list(u'零壹贰叁肆伍陆柒捌玖')
    relation_number = list(u'0123456789')
    return u''.join(random.choice([relation_lower, relation_upper, relation_number])[int(i)] for i in str(digit))


def to_chinese_operator(operator):
    relation = {u'+': u'加', u'-': u'减', u'*': u'乘'}
    return relation[operator]


def chinese_math_challenge():
    operators = (u'+', u'*',)

    payload = {
        'a': random.randint(1, 9),
        'b': random.randint(1, 9),
        'c': random.randint(1, 9),
        'operator': random.choice(operators),
        'operator2': random.choice(operators),
    }

    payload['chinese_a'] = to_chinese_char(payload['a'])
    payload['chinese_b'] = to_chinese_char(payload['b'])
    payload['chinese_c'] = to_chinese_char(payload['c'])
    payload['chinese_operator'] = to_chinese_operator(payload['operator'])
    payload['chinese_operator2'] = to_chinese_operator(payload['operator2'])

    value = eval('{a}{operator}{b}{operator2}{c}'.format(**payload))
    challenge = u'{chinese_a}{chinese_operator}{chinese_b}{chinese_operator2}{chinese_c}等于几'.format(**payload)

    return text_type(challenge), text_type(value)
