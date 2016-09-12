
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var DetailImageSlilck= Class.extend({
                init: function () {
                    console.log('detail image slick begin');
                    this.init_slick();
                },
                init_slick:function(){
                    $('#xs-detail-pic-wrapper').slick({
                        centerMode: true,
                        arrows: true,
                        slidesToShow: 1,
                        slidesToScroll:1,
                        autoplay:false,
                        dots:true
                    });
                }
            });
    return DetailImageSlilck;
});



