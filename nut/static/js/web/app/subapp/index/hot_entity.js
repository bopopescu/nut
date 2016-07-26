
define(['jquery', 'libs/Class','fastdom'], function(
    $, Class,fastdom
){
            var HotEntity= Class.extend({
                init: function () {
                    console.log('begin hot entity ajax js');
                    this.setupScrollEntity();
                },
                setupScrollEntity:function(){
                     $(window).scroll(this.scrollEntityHandler.bind(this));
                },
                scrollEntityHandler:function(){

                }
            });
    return HotEntity;
});



