#encoding=utf8

import requests
import re
from time import time



def test():

    origin_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Referer': 'http://detail.tmall.com/item.htm?id=44691754172'
    }
    s = requests.session();
    r = s.get('http://detail.tmall.com/item.htm?id=44691754172', headers=origin_headers);

    new_header = r.headers;
    new_cookie = r.cookies.get_dict;



    print r.cookies.get_dict();
    print r.headers;



    #
    #
    reg = re.compile('url=\'(\S*)\';');
    m = reg.search(r.text);

    url = m.group(1);

    l = list();
    l.append("callback=setMdskip");
    l.append("timestamp=%d"%int(time()));
    l.append("id=44691754172");
    # l.append("ref=http://detail.tmall.com/item.htm?id=44691754172");
    #
    # #
    # #
    #
    new_url =  "%s&%s"%(url,'&'.join(l))
    # r2 = s.get(new_url, headers=new_header, cookies=new_cookie);
    # print r2.text;
    print new_url;







if __name__ == "__main__":
    test();