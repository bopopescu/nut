
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var CategorySlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('category horizontal scrolling starts !');
                },
                init_slick:function(){
                    $('#category-item-container').slick({
                        arrows: true,
                        //on mobile,set slidesToshow and slidesToScroll like android
                        slidesToShow: 12,
                        slidesToScroll:4,
                        autoplay:false,
                        dots:false,

                        responsive: [
                             {
                                breakpoint: 992,
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
                                    slidesToShow:6,
                                    slidesToScroll:2,
                                    autoplay:false,
                                    dots:false
                                }
                            }
                        ]
                    });
                }
            });
    return CategorySlick;
});



