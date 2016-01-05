define(['libs/Class', 'jquery'], function(Class, $){

    var store2015UrlReg = /store2015/;
    var store2015CookieKey = 'store_2015_cookie_key'

    var TopAd = Class.extend({
        init: function(){
            this.handleTrackerCookie();
            this.handleTopAdDisplay();
            this.initCloseButton();
        },
        initCloseButton: function(){
            $('.top-ad .close-button').click(this.hideTopAd.bind(this));
        },

        handleTrackerCookie: function(){
            if(store2015UrlReg.test(location.href)){
                console.log('access page');
                $.cookie(store2015CookieKey, 'visited', { expires: 7, path: '/' });
            }
        },

        handleTopAdDisplay:function(){
            if($.cookie(store2015CookieKey) === 'visited'){
                return ;
                //console.log('store 2015 page visited');
            }else{
                this.displayTopAd();
            }
        },
        displayTopAd: function(){
            $('.top-ad').slideDown();
        },
        hideTopAd: function(event){
            $('.top-ad .close-button').hide();
            $('.top-ad').slideUp();
        },

    });

    return TopAd;
});