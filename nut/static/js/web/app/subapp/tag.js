define(
    ['libs/Class'],
    function(Class){


        var TagManager = Class.extend({
            init: function(){

            },
            displayTag: function(ele){
                //handle tag display in elements with class "with-tag"
                var ele = ele || document.body;
                var tagContainers = $(ele).find(".with-tag");
                var ereg = /[#＃][0-9a-zA-Z\u4e00-\u9fff\u3040-\u30FF\u30A0-\u30FF]+/g;

                for (var i= 0, tlen=tagContainers.length; i<tlen;i++){
                     var str = tagContainers.eq(i).html(tagContainers.eq(i).html().replace(/\<br[!>]*\>/g, "\n")).text();
                     if (str == undefined){continue;}
                     var cut = str.match(ereg);
                     if (cut == null){
                            tagContainers.eq(i).html(str.replace(/\n/g, "<br>"));
                            continue;
                     }
                    for (var j=0, len=cut.length;j<len; j++){
                        str = str.replace(cut[j], "<a class='btn-link' rel='nofollow' href='/tag/name/"+encodeURI(cut[j].replace(/[#＃]/,""))+"' >"+cut[j]+"</a>&nbsp;");
                    }
                    tagContainers.eq(i).html(str.replace(/\n/g, "<br>"));
                    }
                }

            }

        );

        return TagManager;

});