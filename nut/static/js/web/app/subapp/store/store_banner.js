
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function () {
            console.log('subapp good store start !');
            this.sameHeightFrame('user-latest-article','latest-actions-sidebar');

        },

        sameHeightFrame: function (leftId,rightId) {

            var leftChildHeight = this.getElementHeight(leftId);
            var rightChildHeight = this.getElementHeight(rightId);
            var rightChild = this.getElement(rightId);

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



