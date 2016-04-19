
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
                        centerMode: true,
                        arrows: true,
                        slidesToShow: 6,
                        slidesToScroll:6,
                        autoplay:true,
                        autoplaySpeed:2000,
                        //centerPadding:'18%',
                        dots:false

                        //centerPadding: '60px',
                        //slidesToShow: 3,
                        //responsive: [
                        //    {
                        //        breakpoint: 768,
                        //        settings: {
                        //            centerMode:false,
                        //            slidesToShow:1,
                        //            slidesToScroll:1,
                        //            infinite: true
                        //        }
                        //    },
                        //]
                    });
                }
            });
    return CategorySlick;
});



