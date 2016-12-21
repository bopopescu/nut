def handleRelativeLink(content):
    new_content = content.replace('href="/detail/', 'href="http://www.guoku.com/detail/')
    return new_content

=========================================

@property
def mobile_url(self):
    return 'http://m.guoku.com'+reverse('web_offline_shop_detail',
                                            args=[self.pk])

===========================================

class APIBuyLink(Buy_Link):
    class Meta:
        proxy = True

    def v4_toDict(self):
        res             = self.toDict()
        res.pop('link', None)
        res['buy_link'] = "http://api.guoku.com%s?type=mobile" % reverse('v4_visit_item', args=[self.origin_id])
        res['price']    = int(self.price)
        res['seller']   = self.store_id
        return res

    @property
    def store_id(self):
        if self.origin_source == 'taobao.com':
            m = re.match('http://shop(\d+)\.taobao\.com', self.shop_link)
            if m:
                return m.group(1)
        return ''

================================

def get_taobao_url(taobao_id, is_mobile = False, app_key = None):
    if is_mobile:
        url = "http://a.m.taobao.com/i%s.htm" % taobao_id
    else:
        url = "http://item.taobao.com/item.htm?id=%s" % taobao_id
        if app_key:
            url += "&spm=2014.%s.0.0" % app_key
    return url


=====================

 for row in shows:
            if row.applink in (None, ''):
                pass
            elif row.applink and row.applink.startswith('http://m.guoku.com/articles/'):
                url = row.applink.split('?')
                uri = url[0]
                article_id = uri.split('/')[-2]
                article = APIArticle.objects.get(pk = article_id)

                res['banner'].append(
                    {
                        'url': row.applink,
                        'img':row.image_url,
                        'article': article.v4_toDict(da)
                    }
                )

===========================

if 'taobao' in _origin_source:
            Buy_Link.objects.create(
                entity=entity,
                origin_id=_origin_id,
                cid=_cid,
                origin_source="taobao.com",
                link="http://item.taobao.com/item.htm?id=%s" % _origin_id,
                price=_price,
                default=True,
                shop_link=_shop_link
            )

============================

class TaobaoClient():

    def __init__(self, code, app_key, app_secret):
        self.app_key = app_key
        self.code = code
        self.app_secret = app_secret
        self.redirect_uri = "http://www.guoku.com"

=============================
<p>欢迎访问「果库」网站（隶属于北京果库科技有限公司<a href="http://www.guoku.com">http://www.guoku.com</a>）。我们旨在帮助你发现互联网上最有趣、最人气、最实用的好商品，恪守选品标准和美学格调，开拓精英视野与生活想象。</p>



==============================
        var      host = location.host;
        var      path = '/u/settings/';

        setTimeout(function(){
            window.location = 'http://'+host + path;
        }, 1000);


===========================
<img class="img-responsive" alt="" src="http://imgcdn.guoku.com/{{ sub_category.icon }}" width="64" height="64">

============================

 <a href="http://www.guoku.com" class="logo">

============================
 <a href="http://www.guoku.com/download/" target="_blank" class="new-guoku-blue-btn download-btn-control hidden-sm hidden-md hidden-lg">下载</a>


============================
<li><a href="http://app.guoku.com/download/android/guoku-release.apk"  target="_blank" bi="download_android" _hover-ignore="1" _orighref="http://app.guoku.com/download/android/guoku-release.apk" _tkworked="true" class="fc_4 fs_16">Android 版</a></li>

====================================
def find_entity_hash(str):
    regHash = r'http://www.guoku.com/detail/(\w+)/?$'
    p  = re.compile(regHash)
    m = p.match(str)
    if m :
        return  m.groups()[0]
    else:
        return None


====================================
def mobile_link(value):
   _value = value.decode('utf-8')
   theHash = find_entity_hash(_value)
   if theHash:
        _value = get_mobile_link_by_hash(theHash)
   else:
       pass

   if _value :
        _value = _value.replace('http://www.guoku.com/articles/','http://m.guoku.com/articles/')
        return _value.encode('utf-8')
   else :
       raise Exception('can not find link')
register.filter(mobile_link)


=================
RedirectURI = 'http://www.guoku.com/weixin/auth/'
==================


SITE_HOST = 'http://www.guoku.com'


====================

 showSuccessMessage: function(){
            bootbox.alert(
                {
                    size:'small',
                    message:'验证邮件已经发送, 请阅读邮件，点击邮件中的验证链接后，刷新本页。',
                    className: 'mail-dialog',
                    callback:function(){

                        var host = location.host;
                        var path = location.pathname;
                        window.location = 'http://' + host + path ;
                    }
                }
               );

        },


====================
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');

