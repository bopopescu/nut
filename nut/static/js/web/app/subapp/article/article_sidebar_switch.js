define([
    'libs/Class',
    'jquery'
],function(
    Class,
    $
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
            $('#detail_content_right').removeClass('content-right-show');
            $('#detail_content_right').addClass('content-right-hidden');
            $('.main-article-control').css({
                                             'transform':'translateX('+this.getArticleMoveDistance()+'px)',
                                             '-webkit-transform':'translateX('+this.getArticleMoveDistance()+'px)'
            });
            $('.bottom-article-share').parent('.col-xs-12').css('transform','translateX('+this.getArticleMoveDistance()+'px)');
            $('.sidebar-switch.close-switch').hide();
            $('.sidebar-switch.open-switch').show();
        },
        showSidebar:function(){
            $('#detail_content_right').removeClass('content-right-hidden');
            $('#detail_content_right').addClass('content-right-show');
            $('.main-article-control').css({
                                            'transform':'translateX(0)',
                                            '-webkit-transform':'translateX(0)'
            });
            $('.bottom-article-share').parent('.col-xs-12').css('transform','translateX(0)');
            $('.sidebar-switch.close-switch').show();
            $('.sidebar-switch.open-switch').hide();
        },
        getArticleMoveDistance:function(){
            return this.getSidebarWidth()/2;
        },
        getSidebarWidth:function(){
            return $('#detail_content_right').innerWidth();
        }
    });
    return  ArticleSidebarSwitch;
});
