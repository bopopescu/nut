
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var IndexBgSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('index fade bg slick !');
                },
                init_slick:function(){
                    $('#index_shops_bg_wrapper').slick({
                        dots: false,
                        infinite: true,
                        speed: 500,
                        fade: true,
                        cssEase: 'linear',
                        autoplay: true
                    });
                }

            });
    return IndexBgSlick;
});



