

1. ADD TAOBAO item to youzhan
tb1 = javascript: window.open('http://we.taobao.com/daren/itemPublish.htm?link='+ encodeURIComponent(location.href) + '&name=' + 'notset')

tb2 = javascript: args=location.href.match(/link=(.+)&name/);$('.link-input').val(decodeURIComponent(args[1]));$('.get-item-info').addClass('can-get').click()


2. add guoku item to jiyoujia

need update mng entity edit template , to take effect


jijia1 = javascript: window.open('https://www.jiyoujia.com/youjia/worthbuying/edit.htm?link='+ encodeURIComponent($('#buylinks a')[0].href)+ '&' + 'title=' + encodeURIComponent($('#id_title').val()) + '&' + 'note=' + encodeURIComponent($('.entity-note-table tr td:nth-child(3)').html()) + '&')

jijia2 = javascript: args=location.href.match(/link=(.+?)&/); arg3=location.href.match(/note=(.+?)&/);document.getElementsByClassName('J_countTextarea')[0].value=(decodeURIComponent(arg3[1]));document.getElementsByClassName('J_url')[0].value=(decodeURIComponent(args[1]));document.getElementsByClassName('J_confirmBtn')[0].dispatchEvent(new Event('click'));
jijia2 = javascript: args=location.href.match(/link=(.+?)&/); arg3=location.href.match(/note=(.+?)&/);document.getElementsByClassName('J_countTextarea')[0].value=(decodeURIComponent(arg3[1]));document.getElementsByClassName('J_url')[0].value=(decodeURIComponent(args[1]));document.getElementsByClassName('J_confirmBtn')[0].click();



jijia3 = javascript:arg2=location.href.match(/title=(.+?)&/);document.querySelectorAll('input.J_name')[0].value=(decodeURIComponent(arg2[1]));