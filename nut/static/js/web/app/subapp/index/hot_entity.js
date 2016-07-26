
define(['jquery', 'libs/Class','fastdom'], function(
    $, Class,fastdom
){
    var HotEntity= Class.extend({
        init: function () {
            this.$loading_icon = $('.loading-icon');
            this.$hot_entity_wrapper = $('#hot-entity-list');
            if(this.$hot_entity_wrapper.length > 0){
                this.setupWatcher();
            }else{
                return;
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
            this.screenHeight = window.screen.height;
            this.pageHeight = document.body.scrollHeight;
            this.middleBannerBottom = document.getElementById('hot-entity-list').getBoundingClientRect().bottom;
            this.leftCondition = this.screenHeight + this.scrollTop;
            this.rightCondition = this.pageHeight - this.screenHeight + this.middleBannerBottom;

        },
        doWrite: function(){
            var that = this ;
            if (!this.scrollTop){return ;}
            if (this.leftCondition > this.rightCondition){
                fastdom.write(function(){
                    that.$loading_icon.hide();
                });

            }else{
                fastdom.write(function(){
                    that.$loading_icon.show();
                });
            }
        }
    });
    return HotEntity;
});



