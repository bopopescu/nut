
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var RecommendUserSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('recommend user slick in discover page begin');
                },
                init_slick:function(){
                    $('.recommend-user-list').slick({
                        arrows: true,
                        slidesToShow: 10,
                        slidesToScroll:4,
                        autoplay:true,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:10,
                                    slidesToScroll:3,
                                    autoplay:true,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return RecommendUserSlick;
});



