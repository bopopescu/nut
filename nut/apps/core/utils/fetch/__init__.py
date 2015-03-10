import re

def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None

def parse_jd_id_from_url(url):
    ids = re.findall(r'\d+',url)
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

__author__ = 'edison'
