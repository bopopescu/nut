
define(['jquery', 'libs/Class','libs/slick','fastdom'], function(
    $, Class, slick , fastdom
){
            var MiddlePageBanner= Class.extend({
                init: function () {
                    this.init_slick();
                },
                init_slick:function(){
                    $('#middle-page-banner').slick({
                        centerMode: true,
                        arrows: true,
                        slidesToShow: 1,
                        centerPadding:'18%',
                        dots:false,
                        autoplay: true,
                        autoplaySpeed: 3000,

                        //centerPadding: '60px',
                        //slidesToShow: 3,
                        responsive: [
                            {
                                breakpoint: 768,
                                settings: {
                                    centerMode:false,
                                    slidesToShow:1,
                                    slidesToScroll:1,
                                    infinite: true
                                }
                            }
                        ]
                    }).on('beforeChange', this.beforeSlide.bind(this));
                },

                beforeSlide: function(event,slick,currentSlide,nextSlide){
                            //console.log('before change,currentSlide:');
                            //console.log(currentSlide);
                            //console.log('before change,nextSlide:');
                            //console.log(nextSlide);
                            this.nextSlide = nextSlide;
                            fastdom.write(this.doRenderSlide.bind(this));

                },

                doRenderSlide:function(){
                        $('#middle-page-banner .banner-image-cell').removeClass('gk-slide-current');
                        var selector = '#middle-page-banner .gk-slide-'+  this.nextSlide ;
                        $(selector).addClass('gk-slide-current');
                        //console.log('done');
                }

            });
    return MiddlePageBanner;
});



