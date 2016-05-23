
define(['libs/Class', 'jquery','cookie'], function(Class, $){

    var  destiny_url_test_reg = /store2015/;
    var store2015CookieKey = 'store_2015_cookie_key'
    // here we use a global var isFromMobile, which is bootstraped in base.html (template)

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
            if(destiny_url_test_reg.test(location.href)){
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

            if (!isFromMobile &&(!destiny_url_test_reg.test(location.href))){
                 $('.top-ad').slideDown();
            }

        },
        hideTopAd: function(event){
            $('.top-ad .close-button').hide();
            $('.top-ad').slideUp();
        },

    });

    return TopAd;
});