
define(['libs/Class', 'jquery','cookie'], function(Class, $){

    var  test_url_reg = /20160624/;
    var visited_cookie_key = 'pop_up_store_key'
    // here we use a global var isFromMobile, which is bootstraped in base.html (template)

    var TopAd = Class.extend({
        init: function(){
            this.handleTrackerCookie();
            this.handleTopAdDisplay();
            this.initCloseButton();
        },
        initCloseButton: function(){
            if($('.entity-selection-body').length>0){
                $('.top-ad .close-button').hide();
            }else{
                $('.top-ad .close-button').click(this.hideTopAd.bind(this));
            }
        },

        handleTrackerCookie: function(){
            if(test_url_reg.test(location.href)){
                console.log('access page');
                $.cookie(visited_cookie_key, 'visited', { expires: 7, path: '/' });
            }
        },

        handleTopAdDisplay:function(){
            //if($.cookie(visited_cookie_key) === 'visited'){
            //    return ;
            //    //console.log('store 2015 page visited');
            //}else{
            //    this.displayTopAd();
            //}
            this.displayTopAd();
        },
        displayTopAd: function(){

            if (isFromMobile ||  test_url_reg.test(location.href)){
                //$('.top-ad').hide();
                return ;
            }else{
                 $('.top-ad').slideDown();
            }

            return
        },
        hideTopAd: function(event){
            $('.top-ad .close-button').hide();
            $('.top-ad').slideUp();
        },

    });

    return TopAd;
});