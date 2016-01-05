<<<<<<< HEAD
define(['libs/Class', 'jquery'], function(Class, $){

    var store2015UrlReg = /store2015/;
    var store2015CookieKey = 'store_2015_cookie_key'
=======
define(['libs/Class', 'jquery','cookie'], function(Class, $){

    var  store2015UrlReg = /store2015/;
    var store2015CookieKey = 'store_2015_cookie_key'
    // here we use a global var isFromMobile, which is bootstraped in base.html (template)

>>>>>>> 85b4cd1385e5fd235bec0803dd33f7058b05eda4

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
<<<<<<< HEAD
            $('.top-ad').slideDown();
=======
            if (!isFromMobile){
                 $('.top-ad').slideDown();
            }

>>>>>>> 85b4cd1385e5fd235bec0803dd33f7058b05eda4
        },
        hideTopAd: function(event){
            $('.top-ad .close-button').hide();
            $('.top-ad').slideUp();
        },

    });

    return TopAd;
});