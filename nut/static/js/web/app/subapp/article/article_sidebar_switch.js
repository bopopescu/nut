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
           if($('.sidebar-switch-wrapper').length > 0){
               this.initClickSwitch();
           }
        },
        initClickSwitch:function(){
            $('.sidebar-switch-wrapper').click(this.handleClickSwitch.bind(this));
        },
        handleClickSwitch:function(){
            console.log('hidden sidebar');
            $('#detail_content_right').css({opacity:'0'});
            $('#detail_content .container-fluid').addClass('main-article-control');
            $('.sidebar-switch.close-switch').hide();
            $('.sidebar-switch.open-switch').show();
        }
    });
    return  ArticleSidebarSwitch;
});
