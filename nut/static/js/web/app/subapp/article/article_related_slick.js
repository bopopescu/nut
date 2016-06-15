
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class, slick
){
            var ArticleRelatedSlick= Class.extend({
                init: function () {
                    this.init_slick();
                    console.log('related articles horizontal scrolling starts !');
                },
                init_slick:function(){
                    $('#related-article-container').slick({
                        arrows: true,
                        slidesToShow: 3,
                        slidesToScroll:1,
                        autoplay:false,
                        dots:false,

                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    slidesToShow:2,
                                    slidesToScroll:1,
                                    autoplay:true,
                                    dots:false
                                }
                            }
                        ]
                    });

                }
            });
    return ArticleRelatedSlick;
});



