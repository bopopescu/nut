
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('subapp good store start !');
            this.sameHeightFrame('user-latest-article','latest-actions-sidebar');

        },
        sameHeightFrame:function(leftChildId,rightChildId){
            var leftChildHeight = this.getElementHeight(leftChildId);
            var rightChildHeight = this.getElementHeight(rightChildId);
            if(rightChildHeight > leftChildHeight){
                console.log('right child height is more than left child');
                this.getElement(rightChildId).style.height = leftChildHeight + "px";
            }
        },
        getElementHeight:function(id){
            return this.getElement(id).offsetHeight;
        },
        getElement:function(id){
            return document.getElementById(id);
        }
    });
    return StoreBanner;
});



