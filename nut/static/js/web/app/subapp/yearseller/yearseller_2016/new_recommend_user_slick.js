
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var NewRecommendUserSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('recommend user slick in discover page begin');
                },
                init_slick:function(){
                    $('.new-seller-body .opinions-wrapper.opinions-slick-wrapper').slick({
                        arrows: true,
                        slidesToShow: 6,
                        slidesToScroll:4,
                        autoplay:false,
                        dots:false,

                        responsive: [
                             {
                                breakpoint: 992,
                                settings: {
                                    slidesToShow:6,
                                    slidesToScroll:3,
                                    autoplay:false,
                                    dots:false
                                }
                            },
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:6,
                                    slidesToScroll:3,
                                    autoplay:false,
                                    dots:false
                                }
                            },
                             {
                                breakpoint: 580,
                                settings: {
                                    slidesToShow:3,
                                    slidesToScroll:2,
                                    autoplay:true,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return NewRecommendUserSlick;
});



