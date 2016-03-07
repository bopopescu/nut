
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('subapp good store start !');
            this.sameHeightFrame();

        },
        sameHeightFrame:function(){
            console.log('cry me');
        }
    });
    return StoreBanner;
});



