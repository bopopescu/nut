define(['jquery','libs/underscore','libs/Class','libs/fastdom'],
    function($,_,Class,fastdom){

        var GoTop = Class.extend({
            init: function(){
                this.topLinkWrapper = $('.gotop-wrapper');
                this.topLink = $('.btn-top');
                this.newTopLink = $('.new-btn-top');
                if(this.topLink.length > 0){
                    this.topLinkExist = true;
                }
                if(this.newTopLink.length > 0){
                    this.newTopLinkExist = true;

                }
                if ( this.topLinkExist|| this.newTopLinkExist){
                    this.setupWatcher();
                    if(this.topLinkExist){
                        this.topLink.on('click', function(){
                            $("html, body").animate(
                                {scrollTop : 0}, 800
                            );
                            return false;
                        });
                    }
                    if(this.newTopLinkExist){
                        this.newTopLink.on('click', function(){
                            $("html, body").animate(
                                {scrollTop : 0}, 800
                            );
                            return false;
                        });
                    }
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
                this.scrollTop = $(window).scrollTop();
                if(this.topLinkExist){
                    this.btnRect = this.topLink[0].getBoundingClientRect();
                }
                this.footerRect = $('#guoku_footer')[0].getBoundingClientRect();
            },
            doWrite: function(){
                var that = this ;
                if (!this.scrollTop){return ;}
                if (this.scrollTop > 400 ){

                    fastdom.write(function(){
                        that.topLinkWrapper.show();
                        if(that.topLinkExist){
                            that.topLink.show();
                            if (that.btnRect.bottom >= that.footerRect.top){
                                that.topLink.css({bottom:'370px'});
                            }else{
                                //that.topLink.css({bottom:'170px'});
                            }
                        }

                    });

                }else{
                    fastdom.write(function(){
                        that.topLinkWrapper.hide();
                        that.topLink.hide();
                    });
                }



            }
        });

        return GoTop;
    });