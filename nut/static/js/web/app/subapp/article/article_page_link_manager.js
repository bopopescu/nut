define(['libs/Class','utils/browser', 'jquery'],
    function(Class, browser, $){

        var ArticlePageLinkManager = Class.extend({
            init: function(){
                this.handleWeixinPageLink();
                console.log('')
            },
            handleWeixinPageLink: function(ele){
                var ele = ele || document.body;

                if (browser.is_weixin()){
                    $(ele).find('.mobile-entity-link, .mobile-user-link')
                    .attr('href', 'http://www.guoku.com/download/');
                }
            }

        });

        return ArticlePageLinkManager;

});