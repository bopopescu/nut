
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var RecommendUserSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('recommend user slick in discover page begin');
                },
                init_slick:function(){
                    $('.recommend-user-list,.user-panel-container').slick({
                        arrows: true,
                        slidesToShow: 6,
                        slidesToScroll:4,
                        autoplay:false,
                        dots:false,

                        responsive: [
                             {
                                breakpoint: 992,
                                settings: {
                                    slidesToShow:3,
                                    slidesToScroll:3,
                                    autoplay:false,
                                    dots:false
                                }
                            },
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:8,
                                    slidesToScroll:3,
                                    autoplay:false,
                                    dots:false
                                }
                            },
                             {
                                breakpoint: 580,
                                settings: {
                                    slidesToShow:5,
                                    slidesToScroll:2,
                                    autoplay:false,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return RecommendUserSlick;
});



