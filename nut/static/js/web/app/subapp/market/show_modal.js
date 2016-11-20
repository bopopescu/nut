define(['libs/Class','jquery','bootbox'], function(
    Class,$,bootbox
){
    var ShowModalApp = Class.extend({
        init: function(){
            this.initClickTitleRect();
        },
        initClickTitleRect:function(){
            $('.title-rect').on('click',this.handleTitleRect.bind(this));
        },
        handleTitleRect:function(e){
            var ele = e.currentTarget;
            if($(ele).attr('id') == 'gk_introduce'){
                bootbox.hideAll();
                bootbox.dialog({
                    title: '活动介绍',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'introduce-dialog',
                    message: $('#introduce_modal_content').html()

                });
            }else if($(ele).attr('id') == 'gk_brands'){
                bootbox.hideAll();
                bootbox.dialog({
                    title: '一篓好商品',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'brands-dialog',
                    message: $('#brands_modal_content').html()

                });
            }else if($(ele).attr('id') == 'gk_play'){
                bootbox.hideAll();
                bootbox.dialog({
                    title: '一篓好玩的',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'play-dialog',
                    message: $('#play_modal_content').html()

                });
            }else if($(ele).attr('id') == 'gk_place'){
                bootbox.hideAll();
                bootbox.dialog({
                    title: '活动地点',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'place-dialog',
                    message: $('#place_modal_content').html()

                });
            }else{
                bootbox.hideAll();
                bootbox.dialog({
                    title: '呼朋唤友来玩吧',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'share-dialog',
                    message: $('#share_modal_content').html()

                });
            }
        }
    });

    return ShowModalApp;
});