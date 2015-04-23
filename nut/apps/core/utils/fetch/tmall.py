#encoding=utf8

import requests
import re
from time import time
import json

origin_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Referer': 'http://detail.tmall.com/item.htm?id=44691754172'
    };

# sina_header = {
#                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                   'Accept-Encoding':'gzip, deflate, sdch',
#                   'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
#                   'Cache-Control':'no-cache',
#                   'Connection':'keep-alive',
#                   'Cookie':'U_TRS1=0000003b.8eee2664.528ab39a.a1bea448; U_TRS2=0000003b.8efb2664.528ab39a.7ad30516; SINAGLOBAL=222.129.20.59_1384821765.750894; Apache=222.129.20.59_1384821765.999403; vjuids=2a064f45.1426dcf43ef.0.40a87f13; SessionID=871ut15sso55afris7kl6oabq3; VBLOG_LOGIN=1; SINA_NEWS_CUSTOMIZE_city=%u5317%u4EAC; bgAdCookiezd1010150bp=0; ustat=__222.130.120.206_1413093538_0.15844000; SGUID=1397009324103_21425966; ULV=1415925790328:1:1:1:222.129.20.59_1384821765.999403:; UOR=,,; OPEN_WEBTRENDS_ID=3; mvsign=v%3DML%2FgjhfGL6BMDM51w%2Aw%27; LUP=bt%3D1423662083%26email%3Dtayak%2540sina.com%26f%3D1%26loginname%3Dtayak%26mobile%3D13910291224%26nick%3Dtayak%26nickname%3Dtayak%26uid%3D1404547327%26user%3Dtayak%26ut%3D2015-01-24%2B11%253A39%253A33; LUE=cd407fb6a6e394eda095624a90d4fbab; _s_upa=146; ; bgAdCookiePDPS00000000bg01=0; ULOGIN_IMG=gz-784e50e63adfe6fa8bdece44424ffbe43d45; __utma=269849203.1768757156.1427980164.1427980164.1427980164.1; __utmc=269849203; __utmz=269849203.1427980164.1.1.utmcsr=finance.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; sso_info=v02m6alo5qztKWRk6ClkKSQpZCkiKWRk5SlkJOMpZCjgKWRk5SlkKSYpZCUiKWRk6ClkJSYpZCUkKadlqWkj5OMuYyDlLCNk5ywjbOgwA==; SUB=_2AkMic_KndcNhrABYmP0VyWzia4VH-jjGiefAAX_mJhIxU1R-7SfCT_kV0aeYm0i79Uz1cuKtRI49; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFT1wfAryT6NA_5w1k5Ti3P; xystate=1; xytime=1429582604767; CoupletMedia-1409988133=0; rotatecount=2; vjlast=1429596208; hqEtagMode=0; directAd_samsung=true; ArtiFSize=14; lxlrttp=1429582993'
# }
#
#
#
# sina_header.update(origin_headers);


def get_tmall_header():
    tmall_header = {
        'Cookie':'cna=C6IRC8X/ODgCAd6BFDvWbabx; swfstore=293511; __tmall_fp_ab=__804b; whl=-1%260%260%260; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; lzstat_uv=11965390701316469673|2934243@2674749; lzstat_ss=140379413_3_1398070003_2934243|815277699_0_1422723118_2674749; tkmb=e=zGU0g6e1d7xnyW5gckzC5SRSoSV%2BCJRsbB%2FqUvs5Uf58hRjnchOE8RJiVyxap21Z%2BF5k2ycdFwjLcpg6et5YWldFaIJiTj%2B8PB3D9WtY4uPRMmgp0PWxFg3THzlXWZl9d72ZRUy6HrHElkYSV3L9ohm909Wxn%2B5XYLRmURqimRuTELpeqF6LqRumN4F3VGOHygplmP3ghh8WXWUiIsL4c4lpflo%2BFw6HwYInDAPb8d0rZeab&iv=0&et=1425984084; tk_trace=1; _tb_token_=59d5380e68b33; ck1=; uc1=lltime=1429272638&cookie14=UoW1Hdw4eYlPpw%3D%3D&existShop=false&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=V32FPkk%2Fgipm&tag=4&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; uc3=nk2=F5fFAGakplCe&id2=UU21bCqQ9jo%3D&vt3=F8dAT%2BTo5SBALLi8fWU%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=tayaktaka; tracknick=tayaktaka; cookie2=56e6bb7399ccc24cd086055984b64234; cookie1=ACIJ9hF2im3m%2BNvit%2F8rlnKsDPnZLJknoRP8Hwy%2Fwu4%3D; unb=25737270; t=fafd65949bdd322f75e42578c7769165; _nk_=tayaktaka; _l_g_=Ug%3D%3D; cookie17=UU21bCqQ9jo%3D; login=true; __ozlvd2061=1429594589; CNZZDATA1000279581=1990981142-1429595063-%7C1429595063; ucn=unit; pnm_cku822=043UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt0QHhMeEZ7Qn1GeS8%3D%7CU2xMHDJ7G2AHYg8hAS8WKQcnCU4nTGI0Yg%3D%3D%7CVGhXd1llXGNXb1tvUWxValFuWWRGf0J%2BSnZNdU11QH9FfEl3T3FfCQ%3D%3D%7CVWldfS0TMwcyCysXLQ0jYQ51HEYZaCd8V3dJaVVwJnZYDlg%3D%7CVmhIGCcZOQIiHiEaJQU7DjIKKhYvFisLPwI%2FHyMaIx4%2BCzEPWQ8%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; cq=ccp%3D1; isg=C6C4BA9AD0DB0F423D25D418B73D4637; l=AVS2KrRgVCxULAEZoGGeYVQs1CNULFQs',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    tmall_header.update(origin_headers);
    return tmall_header;

    return
def extract_url(str):
    reg = re.compile('url=\'(\S*)\';');
    m = reg.search(str);
    return m.group(1);


def fix_script_url(script_url):
    l = list();
    l.append("callback=setMdskip");
    l.append("timestamp=%d"%int(time()));
    return  "%s&%s"%(script_url,'&'.join(l))

def get_start_url(id):
    return "http://detail.tmall.com/item.htm?id=%s"%id;

def get_tmall_cookie():

    return {};

def process_mdskip_response(response_str):
    reg = re.compile('\((.*)\)');
    m = reg.search(response_str);
    j_obj = json.loads(m.group(1));
    return  json.dumps(j_obj,sort_keys=True,indent=4, separators=(',', ': '));

def get_price_by_entity_info(entity_info):
    price = 0 ;

    return price ;
    pass


def get_tmall_item_id(id):
    start_url = get_start_url(id);
    with requests.Session() as s :
        r = s.get(start_url , headers  = get_tmall_header(), cookies=get_tmall_cookie());
        # print r.text;
        script_url = extract_url(r.text);
        # print script_url;
        script_url = fix_script_url(script_url);
        # print script_url;
        r = s.get(script_url, headers=get_tmall_header());
        # print r.text;
        entity_info = process_mdskip_response(r.text);
        # print entity_info
        entity_price = get_price_by_entity_info(entity_info);
        # print entity_price
        return entity_price;

def test_final(id):
    start_url = get_start_url(id);
    with requests.Session() as s :
        r = s.get(start_url , headers  = get_tmall_header(), cookies=get_tmall_cookie());
        # print r.text;
        script_url = extract_url(r.text);
        # print script_url;
        script_url = fix_script_url(script_url);
        # print script_url;
        r = s.get(script_url, headers=get_tmall_header());
        # print r.text;

        entity_info = process_mdskip_response(r.text);
        print entity_info;

if __name__ == "__main__":
    test_final(44034481384);