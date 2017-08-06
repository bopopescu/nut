import re
from six.moves import urllib_parse


def parse_taobao_id_from_url(url):
    url_obj = urllib_parse.urlparse(url)
    query_dict = urllib_parse.parse_qs(url_obj.query)
    accept_keys = ('id', 'item_id')
    for key in accept_keys:
        if key in query_dict:
            return query_dict[key][0]
    return None


def parse_jd_id_from_url(url):
    ids = re.findall(r'\d+', url)
    if len(ids) > 0:
        return ids[0]
    else:
        return None


def parse_kaola_id_from_url(url):
    ids = re.findall(r'\d+', url)
    if len(ids) > 0:
        return ids[0]
    else:
        return None


def parse_booking_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split(";"):
        tokens = param.split("=")
        if len(tokens) >= 2 and tokens[0] == "sid":
            return tokens[1]
    return None
