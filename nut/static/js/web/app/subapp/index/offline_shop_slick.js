
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class, slick
){
            var OfflineShopSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('index offline shop init');
                },
                init_slick:function(){
                    $('#offline_shop_container').slick({
                        arrows: true,
                        slidesToShow: 3,
                        slidesToScroll:1,
                        autoplay:false,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 992,
                                settings: {
                                    slidesToShow:2,
                                    slidesToScroll:1,
                                    autoplay:false,
                                    dots:false
                                }
                            },
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
    return OfflineShopSlick;
});



