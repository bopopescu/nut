define(['libs/Class','subapp/account','jquery','fastdom'],
    function(Class,AccountApp,$,fastdom){

    var AppEntityLike = Class.extend({
        init: function(){
            $('#selection, #discover_entity_list, #category-entity-list, #tag-entity-list ,.search-result-list,.authorized-seller-body,.search-entity-item').on('click' ,'.btn-like, .like-action', this.handleLike.bind(this));
            $('.guoku-button .like-action').on('click', this.handleLike.bind(this));

            console.log('app entity like functions');
            console.log(fastdom);
        },
        handleLike:function(e){
            var $likeEle = $(e.currentTarget);
            var $counter = $likeEle.find(".like-count");
            var entity_id = $likeEle.attr("data-entity");
            var $heart = $likeEle.find('i');

            //TODO : gather ga code to tracker app
            if(ga){
                ga('send', 'event', 'button', 'click', 'like', entity_id);
            }
            var url = '';
            if($heart.hasClass('fa-heart-o')){
                url = '/entity/' + entity_id + '/like/';
            }else{
                url = '/entity/' + entity_id + '/unlike/'
            }

            $.when($.ajax({
                url: url,
                method:'POST',
                jsonType:'json'
            })).then(
                function success(data){
                    console.log('success');
                    console.log(data);

                    var count = parseInt($counter.text()) || 0;
                        var result = parseInt(data.status);
                        if (result === 1) {
                            $counter.text(" "+(count + 1));
                            $heart.removeClass('fa-heart-o');
                            $heart.addClass('fa-heart');
                        } else if (result === 0){
                            //console.log(result);

                            if (count >1) {
                                $counter.text(" " + (count - 1));

                            }else{
                                $counter.text(" ");
                            }

                            $heart.removeClass('fa-heart');
                            $heart.addClass('fa-heart-o');
                        } else {
                            // this should be a singleton
                            var accountApp = new AccountApp();
                                accountApp.modalSignIn($(data));
                        }


                }
                ,
                function fail(data){
                    console.log('fail');
                    console.log(data);
                }
            );

        }

    });
    return AppEntityLike;
});