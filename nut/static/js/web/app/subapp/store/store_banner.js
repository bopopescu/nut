
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function () {
            console.log('subapp good store start !');
            this.sameHeightFrame();

        },

        sameHeightFrame: function () {

            var leftChildHeight = this.getElementHeight('user-latest-article');
            var rightChildHeight = this.getElementHeight('latest-actions-sidebar');
            var rightChild = this.getElement('latest-actions-sidebar');

            if (rightChildHeight > leftChildHeight) {
                rightChild.style.height = leftChildHeight + "px";
            }
        },
        getElement:function(id){
            return document.getElementById(id);
        },
        getElementHeight:function(id){
            return this.getElement(id).offsetHeight;

        }

    });
    return StoreBanner;
});



