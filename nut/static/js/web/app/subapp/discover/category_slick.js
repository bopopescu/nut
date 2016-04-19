
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
                        slidesToShow: 6,
                        slidesToScroll:6,
                        autoplay:true,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:3,
                                    slidesToScroll:3,
                                    autoplay:true,
                                    dots:false
                                }
                            }
                        ]
                    });

                }
            });
    return CategorySlick;
});



