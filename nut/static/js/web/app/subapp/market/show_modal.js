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
            if($(ele).attr('id') == 'gk_brands'){
                bootbox.hideAll();
                bootbox.dialog({
                    title: '果库Market 一篓好品牌',
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
                    title: '果库Market 一篓好玩乐',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'play-dialog',
                    message: $('#play_modal_content').html()

                });
            }else{
                bootbox.hideAll();
                bootbox.dialog({
                    title: '果库Market 一篓好心意',
                    onEscape: true,
                    backdrop:true,
                    closeButton: true,
                    animate: true,
                    className: 'love-dialog',
                    message: $('#love_modal_content').html()

                });
            }
        }
    });

    return ShowModalApp;
});