define([
        'libs/Class',
        'jquery',
        'fastdom',
        'cookie'
    ],
    function(Class,$,fastdom,cookie){

    var BottomAd = Class.extend({
        init: function(){
            console.log('bottom ad begin');

            this.scrollTop = null;
            this.lastScrollTop = null;
            this.read = this.write = null;
            this.initHiddenBottomAd();
            this.setupBottomCloseButton();
            this.setupScroll();

        },
        setupBottomCloseButton: function(){
            $('.bottom-ad .close-button').click(function(){
                $('.bottom-ad').addClass('hidden');
            });
        },
        setupScroll: function(){
            $(window).scroll(this.handleBottomAdMove.bind(this));
        },
        handleBottomAdMove:function(){
            var that = this;
            if (!this.read){
                this.read = fastdom.read(function(){
                    that.scrollTop = $(window).scrollTop();
                });
            }

            if(this.write) {
                fastdom.clear(this.write);
            }

            this.write = fastdom.write(this.moveBottomAd.bind(this));
        },
        moveBottomAd:function(){

            if (_.isNull(this.scrollTop)) {
                return ;
            }

            if (_.isNull(this.lastScrollTop)){
                this.lastScrollTop = this.scrollTop;
                return ;
            }

            if(this.lastScrollTop > this.scrollTop){
                this.showBottomAd();
            }else{
                if (this.scrollTop < 140){
                    this.showBottomAd();
                }else{
                    this.hiddenBottomAd();
                }

            }
            this.read = null;
            this.write= null;
            this.lastScrollTop = this.scrollTop;
        },


        checkArticleDetailUrl:function(){
             var testUrl = /articles\/\d+/.test(location.href);
             return testUrl;
        },
        initHiddenBottomAd:function(){
            if(this.checkArticleDetailUrl){
                 $('.bottom-ad').removeClass('showing');
            }
        },
        showBottomAd:function(){
            if(!this.checkArticleDetailUrl()){
                 $('.bottom-ad').addClass('showing');
            }
        },
        hiddenBottomAd:function(){
            if(!this.checkArticleDetailUrl){
                 $('.bottom-ad').removeClass('showing');
            }
        }
    });

    return  BottomAd;

});