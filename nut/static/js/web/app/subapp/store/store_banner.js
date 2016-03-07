
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var StoreBanner= Class.extend({
        init: function(){
            console.log('subapp good store start !');
            this.sameHeightFrame('user-latest-article','latest-actions-sidebar');

        },
        sameHeightFrame:function(leftChildId,rightChildId){
            if(this.getScreenWidth > 767){
                console.log('screen width is more than 767px');
                if(rightChildHeight > leftChildHeight){
                    console.log('right child height is more than left child');
                var leftChildHeight = this.getElementHeight(leftChildId);
                var rightChildHeight = this.getElementHeight(rightChildId);
                this.getElement(rightChildId).style.height = leftChildHeight + "px";
                }
            }
        },
        getElementHeight:function(id){
            return this.getElement(id).offsetHeight;
        },
        getElement:function(id){
            return document.getElementById(id);
        },
        getScreenWidth:function(){
            return document.body.clientWidth;
        }
    });
    return StoreBanner;
});



