# -*- coding:utf-8 -*-
import bleach
from bs4 import BeautifulSoup

articleContentAllowedTags = ['p', 'em', 'strong', 'div', 'ul', \
                             'ol', 'li','a','br','span','img', \
                             'b','blockquote','h3', 'h1','h2',\
                             'h4','dd','dt','center','video']
allowedAttrs = {
    '*': ['class','style'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt'],
}

def handleRelativeLink(content):
    new_content = content.replace('href="/detail/', 'href="http://www.guoku.com/detail/')
    return new_content

def handleEmptyPara(content):
    new_content = content.replace('<p></p>','')
    return new_content

def handleBoldStyle(content):
    soup = BeautifulSoup(content)
    for span in soup.findAll("span",{"style":"font-weight: bold;"}):
        sup = soup.new_tag('b')
        sup.contents = span.contents
        span.insert_after(sup)
        span.extract()
    return str(soup)


def contentBleacher(content):
    content =  handleRelativeLink(content)
    content =  handleBoldStyle(content)
    content =  handleEmptyPara(content)

    return bleach.clean(content, tags=articleContentAllowedTags,\
                                 attributes=allowedAttrs,\
                                 strip_comments=True, strip=True)


wechat_allowed_styles=['font-weight', 'font-style','font-family','color']
from apps.core.utils.bleach import bleach_whitelist as white_lists
def wechatArticleBleacher(content):
    return bleach.clean(content,
                        tags=white_lists.generally_xss_safe,
                        attributes=allowedAttrs,
                        styles=wechat_allowed_styles
                        )



def testHandleRelativeLink():
    content = '<a href="/detail/ffewfwfew/">test</a>'
    print handleRelativeLink(content)

def testHandleBoldStyle():
    content = '<span style="font-weight: bold;">正<span style="font-weight: bold;">few</span>文</span>'
    print handleBoldStyle(content)

def test():
    testHandleRelativeLink()
    testHandleBoldStyle()

if __name__ == '__main__': test()