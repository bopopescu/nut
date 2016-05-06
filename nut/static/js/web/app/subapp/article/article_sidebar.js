define(['jquery','libs/underscore','libs/Class','libs/fastdom'],
    function($,_,Class,fastdom){

        var ArticleSidebar = Class.extend({
            init: function(){
                console.log('article detail dig sidebar');
                this.fixedSidebar = $('.article-sidebar-wrapper');
                if (this.fixedSidebar.length > 0){
                    this.setupWatcher();
                }else{
                    return ;
                }

            },
             setupWatcher:function(){
                $(window).scroll(this.onScroll.bind(this));
            },
            onScroll:function(){
                if(this.read){
                    fastdom.clear(this.read);
                }
                this.read = fastdom.read(this.doRead.bind(this));
                if(this.write){
                    fastdom.clear(this.write);
                }
                this.write = fastdom.write(this.doWrite.bind(this));
            },
            doRead: function(){
                 this.screenHeight = window.screen.height;
                this.shareWrapperTop = $('.share-wrapper')[0].getBoundingClientRect().top;
            },
            doWrite: function(){
                var that = this ;
                if (!this.shareWrapperTop){return ;}
                if (this.shareWrapperTop + 70 <= this.screenHeight){
                    fastdom.write(function(){
                        that.fixedSidebar.addClass('hidden-article-sidebar');
                        that.fixedSidebar.hide();
                    });

                }else{

                    fastdom.write(function(){
                        that.fixedSidebar.removeClass('hidden-article-sidebar');
                        that.fixedSidebar.show();
                    });
                }
            }

        });
        return ArticleSidebar;
    });