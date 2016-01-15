define(['jquery','libs/Class','jqueryeasing'], function($,Class){

    var AnchorScroller = Class.extend({
        init: function(selector){
            $(selector).click(function(event){
                $('html,body').animate({scrollTop: $(this.hash).offset().top - 50}, 1000, 'easeInOutExpo');

                event.preventDefault();
                event.stopPropagation();
                return false;
            });
        }
    });

    return AnchorScroller;
});