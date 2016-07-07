
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var SelectionEntitySlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('selection entity horizontal scrolling starts !');
                },
                init_slick:function(){
                    $('.latest-entity-wrapper')
                        .removeClass('slick-slider')
                        .removeClass('slick-initialized')
                        .slick({
                        arrows: true,
                        slidesToShow: 6,
                        slidesToScroll:4,
                        autoplay:false,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:3,
                                    slidesToScroll:3,
                                    autoplay:false,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return SelectionEntitySlick;
});



