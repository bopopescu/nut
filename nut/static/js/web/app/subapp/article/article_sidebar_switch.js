define([
    'libs/Class',
    'jquery',
    'libs/fastdom'
],function(
    Class,
    $,
    fastdom
){
    var ArticleSidebarSwitch = Class.extend({
        init: function(){
            console.log('article sidebar switch begin');
            this.initClickSwitch();
        },
        initClickSwitch:function(){
            $('.sidebar-switch-wrapper').click(this.handleClickSwitch.bind(this));
        },
        handleClickSwitch:function(){
            if ($('.sidebar-switch.open-switch').css('display') == 'none') {
                this.hiddenSideBar();
            } else {
                this.showSidebar();
            }
        },
        hiddenSideBar:function(){
            //$('#detail_content_right').css({opacity:'0'});
            $('#detail_content_right').hide();
            $('#detail_content .container-fluid').addClass('main-article-control');
            $('.bottom-article-share').parent('.col-xs-12').addClass('bottom-article-share-control');
            $('.sidebar-switch.close-switch').hide();
            $('.sidebar-switch.open-switch').show();
        },
        showSidebar:function(){
            //$('#detail_content_right').css({opacity:'1'});
            $('#detail_content_right').show();
            $('#detail_content .container-fluid').removeClass('main-article-control');
            $('.bottom-article-share').parent('.col-xs-12').removeClass('bottom-article-share-control');
            $('.sidebar-switch.close-switch').show();
            $('.sidebar-switch.open-switch').hide();
        }
    });
    return  ArticleSidebarSwitch;
});
