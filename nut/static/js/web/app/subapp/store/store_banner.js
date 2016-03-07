
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('subapp good store start !');
            this.sameHeightFrame();

        },
        sameHeightFrame:function(){
            var rightChild = document.getElementById('latest-actions-sidebar');
            var rightChildHeight = rightChild.offsetHeight;
            var leftChildHeight = document.getElementById('user-latest-article').offsetHeight;

            if(document.body.clientWidth > 767){
                console.log('more than 767');
                if(rightChildHeight > leftChildHeight){
                    console.log('more than height');
                    rightChild.style.height = leftChildHeight+"px";
                }
            }
        }
    });
    return StoreBanner;
});



