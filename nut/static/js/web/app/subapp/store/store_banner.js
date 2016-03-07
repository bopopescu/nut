
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function () {
            console.log('subapp good store start !');
            this.sameHeightFrame();

        },
        sameHeightFrame: function () {
            var leftChild = document.getElementById("user-latest-article");
            var rightChild = document.getElementById("latest-actions-sidebar");
            var leftChildHeight = leftChild.offsetHeight;
            var rightChildHeight = rightChild.offsetHeight;
            console.log('left height:' + leftChildHeight);
            console.log('right height:' + rightChildHeight);

            if (rightChildHeight > leftChildHeight) {
                console.log('previous right child height:' + rightChildHeight);
                rightChild.style.height = leftChild.offsetHeight + "px";
                console.log('new right child height:' + rightChildHeight);
            }
        }
    });
    return StoreBanner;
});



