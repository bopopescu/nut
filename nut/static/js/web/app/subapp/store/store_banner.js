
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function () {
            this.init_slick();
            console.log('subapp good store start !');
            //this.sameHeightFrame('user-latest-article','latest-actions-sidebar');
        },
        init_slick:function(){
            $('#index-banners').slick({
                centerMode: true,
                arrows: true,
                slidesToShow: 1,
                centerPadding:'18%',
                dots:false,

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
                    },
                ]
            }).on(
                'beforeChange',function(event,slick,currentSlide,nextSlide){
                    console.log('before change,currentSlide:');
                    console.log(currentSlide);
                    console.log('before change,nextSlide:');
                    console.log(nextSlide);
                    console.log(nextSlide instanceof jQuery);
                    var currentSlideToo = $('#index-banners').slick('slickCurrentSlide');
                    console.log(currentSlideToo);
                }).on(
                'afterChange',function(event,slick,currentSlide){
                    console.log('after change,currentSlide:');
                    console.log(currentSlide);
                }
            );
        },

        //sameHeightFrame: function (leftId,rightId) {
        //    var leftChildHeight = this.getElementHeight(leftId);
        //    var rightChildHeight = this.getElementHeight(rightId);
        //    var rightChild = this.getElement(rightId);
        //    if (rightChildHeight > leftChildHeight) {
        //        rightChild.style.height = leftChildHeight + "px";
        //    }
        //},
        //getElement:function(id){
        //    return document.getElementById(id);
        //},
        //getElementHeight:function(id){
        //    return this.getElement(id).offsetHeight;
        //}
    });
    return StoreBanner;
});



