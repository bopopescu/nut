define(['jquery', 'libs/Class', 'subapp/article/article_page_link_manager'],
    function($, Class, ArticlePageLinkManager){
        var CardRender = Class.extend({
            init: function(){
                this.renderEntityCards();
                this.articlePageLinkManager = new ArticlePageLinkManager();
            },
            renderEntityCards: function(){
                var that = this ;
                var cardList = $('.guoku-card');
                 $.map(cardList, function(ele, index){
                    var hash = $(ele).attr('data_entity_hash');
                    if (hash){
                        var url = '/detail/' + hash + '/card/'
                        $.when($.ajax({
                            url: url,
                            method: 'GET'
                        })).then(
                            function success(data){
                                //console.log("load card success");
                                if(data.error == 0){
                                    //console.log('card data ok ');
                                    var newInnerHtml = $(data.html).html();
                                    //console.log(newInnerHtml);
                                    $(ele).html(newInnerHtml);
                                    that.articlePageLinkManager.handleWeixinPageLink(ele);
                                    console.log('card rendered');
                                }
                                else{
                                    console.log('card data error');
                                }

                            },function fail(){
                                console.log("load card fail!!");
                            });
                    }
                });
            }
        });

        return CardRender;

});