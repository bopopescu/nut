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
            console.log('article width:'+this.getArticleContainerWidth());
            console.log('screen width:'+this.getScreenWidth());
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
            $('#detail_content .container-fluid').first().addClass('main-article-control');
             $('#detail_content .container-fluid').first().css('transform','translateX('+this.getArticleMoveDistance()+'px)');
            $('.bottom-article-share').parent('.col-xs-12').addClass('bottom-article-share-control');
            $('.sidebar-switch.close-switch').hide();
            $('.sidebar-switch.open-switch').show();
        },
        showSidebar:function(){
            //$('#detail_content_right').css({opacity:'1'});
            $('#detail_content_right').show();
            $('#detail_content .container-fluid').first().removeClass('main-article-control');
            $('.bottom-article-share').parent('.col-xs-12').removeClass('bottom-article-share-control');
            $('.sidebar-switch.close-switch').show();
            $('.sidebar-switch.open-switch').hide();
        },
        getArticleMoveDistance:function(){
            return (this.getScreenWidth()-this.getArticleContainerWidth())/2;
        },
        getArticleContainerWidth:function(){
            return $('#detail_content .container-fluid').first().width();
        },
        getScreenWidth:function(){
            return window.screen.width;
        }
    });
    return  ArticleSidebarSwitch;
});
