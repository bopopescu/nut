
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var ColumnsSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('columns slick begin');
                },
                init_slick:function(){
                    $('#columns .columns-wrapper.hidden-xs').slick({
                        arrows: true,
                        slidesToShow: 1,
                        slidesToScroll:1,
                        autoplay:false,
                        dots:false
                    });
                }
            });
    return ColumnsSlick;
});



