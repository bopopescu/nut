define(['bootstrap',
        'libs/Class',
        'underscore',
        'jquery',
        'fastdom',
        'cookie',
        'subapp/top_ad/top_ad',
        'subapp/top_notification/top_notification'
    ],
    function(boot, Class,_,$,fastdom,cookie,TopAd,TopNotification){

    // cookie is a shim resource , it will attch to jquery objects.

     function show_sns_page_dot(){
            $('.nav-user-actions .round').css({display:'inline-block'});
            $('.setting-list .round').css({display: 'inline-block'});
    };
    function hide_sns_page_dot(){
            $('.nav-user-actions .round').css({display:'none'});
            $('.setting-list .round').css({display: 'none'});

    };


    var Menu = Class.extend({
        init: function(){

            ///////////////////////////
            //console.log('in Menu init, ');
            //console.log(jQuery);
            ////////////////////////////

            this.$menu = $('#guoku_main_nav');
            this.fixMenuCondition = null;
            this.scrollTop = null;
            //this.lastScrollTop = null;
            this.read = this.write = null;
            this.initHiddenBottomAd();
            this.setupScrollMenu();
            this.checkSNSBindVisit();
            this.checkEventRead();
            //this.topAd = new TopAd();
            this.topNotification = new TopNotification();
            this.setupBottomCloseButton();

        },
        setupBottomCloseButton: function(){
            $('.bottom-ad .close-button').click(function(){
                $('.bottom-ad').addClass('hidden');
            });
        },
        checkEventRead:function(){
            // add by an , for event link status check , remove the red dot if event is read.
            // the key is defined in 2 places!  DRY...
            var viewed_event_slug_cookie_key = 'viewed_event_slug_cookie_key';
            if(!newest_event_slug){
                return ;
            }
            if ($.cookie(viewed_event_slug_cookie_key) === newest_event_slug){
                //console.log('event is read!');
                jQuery('.nav [href="/event/"] .round').css({display:'none'});
            }else{
                jQuery('.nav [href="/event/"] .round').css({display:'inline-block'});
            }

            return ;
        },
        checkSNSBindVisit: function(){
            var sns_bind_page_visited_key = 'SNS_BIND_PAGE_VISITED';
            if ($.cookie(sns_bind_page_visited_key) === 'visited'){
                hide_sns_page_dot();
            }else{
                show_sns_page_dot();
            }
        },

        setupScrollMenu: function(){
            $(window).scroll(this.scheduleHeaderMove.bind(this));
            //$(window).scroll(_.debounce(this.show.bind(this), 100));
        },
        scheduleHeaderMove:function(){
            var that = this;
            if (!this.read){
                this.read = fastdom.read(function(){
                    that.scrollTop = $(window).scrollTop();
                    that.screenHeight = window.screen.height;
                    that.fixMenuCondition = $('#guoku_main_nav')[0].getBoundingClientRect().height - 50;
                    if($('#main_article').length){
                          that.articleHeight = $('#main_article')[0].getBoundingClientRect().height;
                    }
                    that.pageHeight = document.body.scrollHeight;
                    that.hiddenLeftCondition = that.screenHeight + that.scrollTop;
                    that.hiddenRightCondition = that.articleHeight + 102;

                });
            }

            if(this.write) {
                fastdom.clear(this.write);
            }

            this.write = fastdom.write(this.moveHeader.bind(this));
        },
        moveHeader:function(){
            //console.log('move header');

            if (_.isNull(this.scrollTop)) {
                return ;
            }

            if(this.scrollTop > this.fixMenuCondition){
                this.fixMenu();
            }else{
                this.removeFixMenu();
            }

            //if (_.isNull(this.lastScrollTop)){
            //    this.lastScrollTop = this.scrollTop;
            //    return ;
            //}

            if(this.lastScrollTop > this.scrollTop){
                this.showHeader();
                this.showBottomAd();
            }else{
                if (this.scrollTop < 140){
                    this.showHeader();
                    this.showBottomAd();
                }else{
                     this.hideHeader(this.scrollTop);
                    this.hiddenBottomAd();
                }

            }
            if(this.hiddenLeftCondition > this.hiddenRightCondition){
                this.hideHeader();
                 this.hiddenBottomAd();
            }

            this.read = null;
            this.write= null;
            //this.lastScrollTop = this.scrollTop;
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
        },
        showHeader: function(){
            //console.log('show header');
            //this.$menu.removeClass('hidden-header');
            //this.$menu.addClass('shown-header');
            $('.round-link').show();
            $('.bottom-article-share-wrapper').removeClass('hidden-animation');

            //console.log((new Date()).getMilliseconds());

        },
        hideHeader: function(){
            //console.log('hideHeader');
            //this.$menu.removeClass('shown-header');
            //this.$menu.addClass('hidden-header');
            $('.round-link').hide();
            $('.bottom-article-share-wrapper').addClass('hidden-animation');

            //console.log((new Date()).getMilliseconds());
        },
        fixMenu:function(){
            this.$menu.addClass('fix-new-index-navbar');
            if($('.top-search-wrapper').length){
                $('.top-search-wrapper').addClass('hidden');
            }
        },
        removeFixMenu:function(){
            if(this.$menu.hasClass('fix-new-index-navbar')){
                 if($('.top-search-wrapper').length) {
                     $('.top-search-wrapper').removeClass('hidden');
                 }
                 this.$menu.removeClass('fix-new-index-navbar');
            }
        }
    });

    return  Menu;

});