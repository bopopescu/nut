define(['jquery', 'libs/Class'],
    function($, Class){
        var CardRender = Class.extend({
            init: function(){
                this.renderEntityCards();
            },
            renderEntityCards: function(){
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
                                    var newInnerHtml = $(data.html).html()
                                    //console.log(newInnerHtml);
                                    $(ele).html(newInnerHtml);
                                    //console.log('card rendered');
                                }
                                else{
                                    console.log('card data error');
                                }

                            },function fail(){
                                console.log("load card fail");
                            });
                    }
                });
            }
        });

        return CardRender;

});