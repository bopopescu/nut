define(['jquery','libs/Class','jqueryeasing'], function($,Class){

    var ArticleLinkScroll = Class.extend({
        init: function(selector){
            console.log('article remark link scroll');
            $(selector).click(function(event){
                $('html,body').animate({scrollTop: $(this.hash).offset().top - 40}, 1000, 'easeInOutExpo');
                event.preventDefault();
                event.stopPropagation();
                return false;
            });
        }
    });

    return ArticleLinkScroll;
});