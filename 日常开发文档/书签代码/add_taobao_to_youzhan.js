


tb1 = javascript: window.open('http://we.taobao.com/daren/itemPublish.htm?link='+ encodeURIComponent(location.href) + '&name=' + 'notset')

tb2 = javascript: args=location.href.match(/link=(.+)&name/);$('.link-input').val(decodeURIComponent(args[1]));$('.get-item-info').addClass('can-get').click()
