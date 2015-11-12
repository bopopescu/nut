define(['libs/Class',
        'subapp/account',
        'jquery',
        'fastdom',
        'underscore',
        'subapp/account'
    ],
    function (Class,
              AccountApp,
              $,
              fastdom,
              _,
              AccountApp) {

        var AppArticleDig = Class.extend({
            init: function () {

                $('.dig-action').on('click', this.handleDig.bind(this));

            },
            handleDig: function (e) {
                var $digEle = $(e.currentTarget);
                var action = $digEle.hasClass('undigged')? 'dig': 'undig';
                    articleId = $digEle.attr('data-article-id');
                $.when(this.sendRequest(articleId,action)).then(
                    this.requestSuccess.bind(this),
                    this.requestFail.bind(this)
                );
                    console.log(articleId);
            },
            getRequestUrl:function(articleId, action){
                var url = '/articles/'+ articleId + '/' + action + '/';
                return url ;
            },
            sendRequest: function(articleId, action){
                var requestUrl = this.getRequestUrl(articleId, action);
                return $.ajax({
                    method: 'POST',
                    url: requestUrl,
                });

            },

            getAccountApp:function(){
                this.AccountApp = this.AccountApp || new AccountApp();
                return this.AccountApp;
            },
            requestSuccess: function(data){

                if(_.isString(data)){
                    this.getAccountApp().modalSignIn(data);
                    return ;
                }
                this.updateDigElementStatus(data);
            },
            updateCounter: function($counterEle, status){
                if(!$counterEle || ($counterEle.length === 0)){
                    return ;
                }
                var html = $counterEle.html();
                if (!html){
                    html = '0';
                }
                var currentCount =  parseInt(html);
                if (_.isNaN(currentCount)){
                    currentCount = 0 ;
                };

                if (status === 1){
                    currentCount +=1 ;
                }else if(status === 0){
                    currentCount -=1;
                }else{
                    console.log('error parse dig count');
                }

                if(currentCount<=0){
                    $counterEle.html('  ');
                }else{
                    $counterEle.html(currentCount + ' ');
                }



            },
            updateDigClass: function($ele, status){
                if(status === 1){
                    $ele.removeClass('undigged')
                        .addClass('digged');
                }else if(status === 0){
                    $ele.removeClass('digged')
                        .addClass('undigged');
                }else{
                    console.log('status error for dig wrapper！');
                }
            },
            updateDigElementStatus: function(data){
                var that = this;
                var article_id = data.article_id;
                var dig_elements = $('.dig-action[data-article-id="'+  article_id  +'"]');
                var status = data.status;
                    dig_elements.each(function(index,ele){
                      that.updateCounter($(ele).parent().find('.dig-count'), status);
                      that.updateDigClass($(ele), status);
                    });
            },
            requestFail:function(){
                console.log('server error');
            }
        });

        return AppArticleDig;


    });