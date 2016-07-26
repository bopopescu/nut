
define(['jquery', 'libs/Class','fastdom'], function(
    $, Class,fastdom
){
    var HotEntity= Class.extend({
        init: function () {
            this.$loading_icon = $('.loading-icon');
            this.$hot_entity_wrapper = $('#hot-entity-list');
            this.should_load_hot_entity = 0;
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
            this.pageScrollLength = this.screenHeight + this.scrollTop;
            this.middleBannerPosition = this.pageHeight - this.screenHeight + this.middleBannerBottom;

        },
        doWrite: function(){
            var that = this ;
            if (!this.scrollTop){return ;}
            if (this.pageScrollLength > this.middleBannerPosition && this.should_load_hot_entity == 0){
                this.postAjaxRequest();

                //fastdom.write(function(){
                //    that.$loading_icon.hide();
                //});

            }else{
                //fastdom.write(function(){
                //    that.$loading_icon.show();
                //});
            }
        },
        postAjaxRequest:function(){
            this.should_load_hot_entity=1;
            $.when(
                $.ajax({
                    cache:true,
                    type:"get",
                    url: '/index_hot_entity/',
                    data: ''
                })
            ).then(
                this.postSuccess.bind(this),
                this.postFail.bind(this)
            );
        },
        postSuccess:function(result){
            console.log('post request success.');
            var status = parseInt(result.status);
            if(status == 1){
                 this.$loading_icon.hide();
                 this.showHotEntity($(result.data));
            }else{
                this.$loading_icon.hide();
                this.showFail(result);
            }
        },
        postFail:function(result){
            console.log('post fail');
        },
        showFail:function(result){
            console.log('get ajax data failed');
        },
        showHotEntity: function(elemList){
            console.log('get ajax data success');
            //this.$hot_entity_wrapper.empty();
            this.$hot_entity_wrapper.append(elemList);
        }
    });
    return HotEntity;
});



