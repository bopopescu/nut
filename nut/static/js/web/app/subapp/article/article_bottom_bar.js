define([
        'libs/Class',
        'jquery',
        'fastdom'
    ],
    function(Class,$,fastdom){
        
    var ArticleBottomBar = Class.extend({
        init: function(){
            console.log('article bottom bar begin');
            
            this.scrollTop = null;
            this.lastScrollTop = null;
            this.read = this.write = null;
            
            this.setupScroll();
        },
        
        setupScroll: function(){
            $(window).scroll(this.articleBottomBarMove.bind(this));
        },
        articleBottomBarMove:function(){
            var that = this;
            if (!this.read){
                this.read = fastdom.read(function(){
                    if($('#main_article').length){
                          that.articleHeight = $('#main_article')[0].getBoundingClientRect().height;
                    }
                    that.scrollTop = $(window).scrollTop();
                    that.screenHeight = window.screen.height;
                    that.hiddenLeftCondition = that.screenHeight + that.scrollTop;
                    that.hiddenRightCondition = that.articleHeight + 102;
                });
            }

            if(this.write) {
                fastdom.clear(this.write);
            }

            this.write = fastdom.write(this.moveArticleBottomBar.bind(this));
        },
        moveArticleBottomBar:function(){

            if (_.isNull(this.scrollTop)) {
                return ;
            }

            if (_.isNull(this.lastScrollTop)){
                this.lastScrollTop = this.scrollTop;
                return ;
            }

            if(this.lastScrollTop > this.scrollTop){
                this.showArticleBottomBar();
            }else{
                if (this.scrollTop < 140){
                    this.showArticleBottomBar();
                }else{
                     this.hideArticleBottomBar(this.scrollTop);
                }
            }
            if(this.hiddenLeftCondition > this.hiddenRightCondition){
                this.hideArticleBottomBar();
            }

            this.read = null;
            this.write= null;
            this.lastScrollTop = this.scrollTop;
        },
        showArticleBottomBar: function(){
            $('.bottom-article-share-wrapper').removeClass('hidden-animation');
        },
        hideArticleBottomBar: function(){
            $('.bottom-article-share-wrapper').addClass('hidden-animation');
        }
    });

    return  ArticleBottomBar;

});