define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var CategorySlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('entity horizontal scrolling starts !');
                },
                init_slick:function(){
                    $('#recommend-entity-wrapper').slick({
                        arrows: true,
                        slidesToShow: 6,
                        slidesToScroll:3,
                        autoplay:true,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:3,
                                    slidesToScroll:1,
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