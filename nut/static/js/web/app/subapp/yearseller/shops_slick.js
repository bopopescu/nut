
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var ShopsSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('shops slick begin');
                },
                init_slick:function(){
                    $('#shops .shops-slick-wrapper').slick({
                        arrows: true,
                        slidesToShow: 4,
                        slidesToScroll:3,
                        autoplay:false,
                        dots:false,

                        responsive: [
                             {
                                breakpoint: 992,
                                settings: {
                                    slidesToShow:2,
                                    slidesToScroll:2,
                                    autoplay:false,
                                    dots:false
                                }
                            },
                            //{
                            //    breakpoint: 768,
                            //    settings: {
                            //        slidesToShow:1,
                            //        slidesToScroll:1,
                            //        autoplay:false,
                            //        dots:false
                            //    }
                            //},
                             {
                                breakpoint: 580,
                                settings: {
                                    slidesToShow:1,
                                    slidesToScroll:1,
                                    autoplay:false,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return ShopsSlick;
});



