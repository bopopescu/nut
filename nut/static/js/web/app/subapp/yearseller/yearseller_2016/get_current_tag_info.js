
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var GetCurrentTagInfo= Class.extend({
                init: function () {
                    this.initSetCurrentTagInfo();
                    console.log('index fade bg slick !');
                },
                initSetCurrentTagInfo:function(){
                    currentTagInfo = this.getCurrentTagInfo();
                    if(currentTagInfo){
                        $('.topic-tag-desc-wrapper .tag-desc').text(currentTagInfo);
                    }
                },
                getCurrentTagInfo:function(){
                    return $('#top_article_tags_container .top-article-tag .tag-element.tag-current ').parent().attr('title');
                }


            });
    return GetCurrentTagInfo;
});



