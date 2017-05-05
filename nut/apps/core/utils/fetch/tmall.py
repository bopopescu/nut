# -*- coding: utf-8 -*-

import requests
import re
from time import time
import json

cookies = {
    'CNZZDATA1000279581': '1990981142-1429595063-%7C1429595063',
    '__ozlvd2061': '1429594589',
    '__tmall_fp_ab': '__804b',
    '_l_g_': 'Ug%3D%3D',
    '_nk_': '%5Cu5F20%5Cu4FCA%5Cu950B_zz',
    '_tb_token_': 'nNgfbHqmeeIL',
    'ck1': '',
    'cna': '6D5REVF5xxwCAW/A8EUANM5H',
    'cookie17': 'VAiW4Tb5kVM%3D',
    'cookie1': 'UNkweTPU3EgZXRheWGPctSRirqmI%2FAmjDBi%2FLGH5wys%3D',
    'cookie2': '509a61b3cf8c60e7a16f54708525454c',
    'cq': 'ccp%3D1',
    'isg': 'AjQ0Y-zz0W5vMkRhLm3WMTUcBfT-fFj3V1t2vs6VwL9COdSD9h0oh-r7y8se',
    'l': 'Au/vszFvCl6Dsnowaymih3CT/xj5lEO2',
    'lgc': '%5Cu5F20%5Cu4FCA%5Cu950B_zz',
    'login': 'true',
    'lzstat_ss': '140379413_3_1398070003_2934243|815277699_0_1422723118_2674749',
    'lzstat_uv': '11965390701316469673|2934243@2674749',
    'otherx': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
    'pnm_cku822': '043UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt0QHhMeEZ7Qn1GeS8%3D%7CU2xMHDJ7G2AHYg8hAS8WKQcnCU4nTGI0Yg%3D%3D%7CVGhXd1llXGNXb1tvUWxValFuWWRGf0J%2BSnZNdU11QH9FfEl3T3FfCQ%3D%3D%7CVWldfS0TMwcyCysXLQ0jYQ51HEYZaCd8V3dJaVVwJnZYDlg%3D%7CVmhIGCcZOQIiHiEaJQU7DjIKKhYvFisLPwI%2FHyMaIx4%2BCzEPWQ8%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
    'swfstore': '293511',
    't': '817f38f3a470e0a9538701f7f70815d3',
    'tk_trace': '1',
    'tkmb': 'e=zGU0g6e1d7xnyW5gckzC5SRSoSV%2BCJRsbB%2FqUvs5Uf58hRjnchOE8RJiVyxap21Z%2BF5k2ycdFwjLcpg6et5YWldFaIJiTj%2B8PB3D9WtY4uPRMmgp0PWxFg3THzlXWZl9d72ZRUy6HrHElkYSV3L9ohm909Wxn%2B5XYLRmURqimRuTELpeqF6LqRumN4F3VGOHygplmP3ghh8WXWUiIsL4c4lpflo%2BFw6HwYInDAPb8d0rZeab&iv=0&et=1425984084',
    'tracknick': '%5Cu5F20%5Cu4FCA%5Cu950B_zz',
    'uc1': 'cookie14=UoW%2Bu4%2BAHegk2Q%3D%3D&cookie21=UIHiLt3xTIkz&cookie15=UtASsssmOIJ0bQ%3D%3D',
    'uc3': 'sg2=UtRWCDgLIo9YOUj8uI992MhO7WiLVBdWPbjabycmm18%3D&nk2=ttQ7Kg%2FQvD6%2B&id2=VAiW4Tb5kVM%3D&vt3=F8dARVEHS%2FVAvjZesn4%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D',
    'ucn': 'unit',
    'unb': '79169971',
    'whl': '1%260%260%260',
}


def _get_tmall_header():

    tmall_header = {
        'Cookie': ' '.join('{}={}'.format(key, value) for key, value in cookies.iteritems()),
        # 'Cookie': 'sm4=110100 uc3=nk2=ttQ7Kg%2FQvD6%2B&id2=VAiW4Tb5kVM%3D&vt3=F8dARVEHT8eQpVHUSGM%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; uss=WvFaos8VGai5kVxg9L0MyQvzZrw3Y%2BsvbfEXVnXR%2FqxlRI3mJWJvko3wag%3D%3D; lgc=%5Cu5F20%5Cu4FCA%5Cu950B_zz; tracknick=%5Cu5F20%5Cu4FCA%5Cu950B_zz; unb=79169971; skt=88cdd2965432d248; t=817f38f3a470e0a9538701f7f70815d3; _l_g_=Ug%3D%3D; _nk_=%5Cu5F20%5Cu4FCA%5Cu950B_zz; _tb_token_=nNgfbHqmeeIL; login=true; cq=ccp%3D0; cna=6D5REVF5xxwCAW/A8EUANM5H; pnm_cku822=169UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FQXtFfEN8Rn1EfCo%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAkUsR2k%2FaQ%3D%3D%7CVGhXd1llXGhWbFJrVGtRalNrXGFDfkF4QHVJcUx1T3BEcUh8R39Faz0%3D%7CVWldfS0QMAU5DS0RLQ0jB30OawovGWUcdycJXwk%3D%7CVmhIGCcZORgkBDgBOAUlGyAbJgY6AzoHJxMuEzMPNg8yEicbJ3En%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; l=AjAwaI6D9lHp4aJudQR1c6uSgPSDhxST; isg=At_f4tcz-p6Yj_9AMbTNoAIFbjWQRzPmd8GYr3EthA6FAP6CeBZiNlOStCeE',
        # 'Cookie': 'cna=C6IRC8X/ODgCAd6BFDvWbabx swfstore=293511 __tmall_fp_ab=__804b whl=-1%260%260%260 otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0 lzstat_uv=11965390701316469673|2934243@2674749 lzstat_ss=140379413_3_1398070003_2934243|815277699_0_1422723118_2674749 tkmb=e=zGU0g6e1d7xnyW5gckzC5SRSoSV%2BCJRsbB%2FqUvs5Uf58hRjnchOE8RJiVyxap21Z%2BF5k2ycdFwjLcpg6et5YWldFaIJiTj%2B8PB3D9WtY4uPRMmgp0PWxFg3THzlXWZl9d72ZRUy6HrHElkYSV3L9ohm909Wxn%2B5XYLRmURqimRuTELpeqF6LqRumN4F3VGOHygplmP3ghh8WXWUiIsL4c4lpflo%2BFw6HwYInDAPb8d0rZeab&iv=0&et=1425984084 tk_trace=1 _tb_token_=59d5380e68b33 ck1= uc1=lltime=1429272638&cookie14=UoW1Hdw4eYlPpw%3D%3D&existShop=false&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=V32FPkk%2Fgipm&tag=4&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0 uc3=nk2=F5fFAGakplCe&id2=UU21bCqQ9jo%3D&vt3=F8dAT%2BTo5SBALLi8fWU%3D&lg2=WqG3DMC9VAQiUQ%3D%3D lgc=tayaktaka tracknick=tayaktaka cookie2=56e6bb7399ccc24cd086055984b64234 cookie1=ACIJ9hF2im3m%2BNvit%2F8rlnKsDPnZLJknoRP8Hwy%2Fwu4%3D unb=25737270 t=fafd65949bdd322f75e42578c7769165 _nk_=tayaktaka _l_g_=Ug%3D%3D cookie17=UU21bCqQ9jo%3D login=true __ozlvd2061=1429594589 CNZZDATA1000279581=1990981142-1429595063-%7C1429595063 ucn=unit pnm_cku822=043UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt0QHhMeEZ7Qn1GeS8%3D%7CU2xMHDJ7G2AHYg8hAS8WKQcnCU4nTGI0Yg%3D%3D%7CVGhXd1llXGNXb1tvUWxValFuWWRGf0J%2BSnZNdU11QH9FfEl3T3FfCQ%3D%3D%7CVWldfS0TMwcyCysXLQ0jYQ51HEYZaCd8V3dJaVVwJnZYDlg%3D%7CVmhIGCcZOQIiHiEaJQU7DjIKKhYvFisLPwI%2FHyMaIx4%2BCzEPWQ8%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D cq=ccp%3D1 isg=C6C4BA9AD0DB0F423D25D418B73D4637 l=AVS2KrRgVCxULAEZoGGeYVQs1CNULFQs',
        'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'Referer': 'http://detail.tmall.com/item.htm?id=544201668379'
    }
    return tmall_header


def _get_script_url(source_html):
    reg = re.compile('url=\'(\S*)\'')
    m = reg.search(source_html)
    script_url = m.group(1)
    script_url = script_url.split('\'')[0]

    protocol = 'https:' if 'https:' not in script_url else ''

    extra_params = ['callback=setMdskip', 'timestamp={}'.format(time())]
    return "{}{}&{}".format(protocol, script_url, '&'.join(extra_params))


def _process_mdskip_response(response_str):
    reg = re.compile('\((.*)\)')
    m = reg.search(response_str)
    j_obj = json.loads(m.group(1))
    return j_obj


def _get_price_by_entity_info(entity_info):
    prices = []

    if entity_info['isSuccess']:
        try:
            price_info = entity_info['defaultModel']['itemPriceResultDO']['priceInfo']
            for k, v in price_info.iteritems():
                prices.append(price_info[k]['price'])
                # may be there is multiple promotionList ... TODO
                if price_info[k].get('promotionList') and len(price_info[k].get('promotionList')):
                    # if priceInfo[k]['promotionList'] and len(priceInfo[k]['promotionList']):
                    for promo in price_info[k]['promotionList']:
                        try:
                            prices.append(promo['price'])
                            prices.append(promo['extraPromPrice'])
                        except KeyError:
                            continue
                elif price_info[k].get('suggestivePromotionList'):
                    try:
                        prices.append(price_info[k].get('suggestivePromotionList')[0]['price'])
                    except KeyError:
                        continue

        except Exception as e:
            # TODO: log error
            pass

        finally:
            if len(prices) > 0:
                price = min(map(float, prices))
            else:
                price = 0
    else:
        price = 0

    return price


def get_tmall_item_price(item_id):
    start_url = "http://detail.tmall.com/item.htm?id={}".format(item_id)
    with requests.Session() as session:

        # set cookies
        for key, value in cookies.iteritems():
            session.cookies[key] = value

        resp = session.get(url=start_url,
                           verify=False,
                           headers=_get_tmall_header())

        return get_price(resp.text, session)


def get_price(source_html, session):
    entity_price = 0
    try:
        resp = session.get(url=_get_script_url(source_html),
                           headers=_get_tmall_header())

        # 价格为0时需要cookie中的账户登陆, 登录之后就能取到价格 ???
        if 'window.location' in resp.text:
            print(resp.text)
            return entity_price
        entity_info = _process_mdskip_response(resp.text)
        entity_price = _get_price_by_entity_info(entity_info)

    except Exception as e:
        # TODO : log the exception
        pass

    return entity_price


if __name__ == "__main__":
    print(get_tmall_item_price('544201668379'))
