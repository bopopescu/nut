
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var AnnualReport= Class.extend({
        init: function () {
            console.log('hello rose.write codes here');
            console.log(this.getPageHeight());
            console.log(this.getScrollHeight);
            console.log(this.getFooterHeight('guoku_footer'));

        },
        hideReport:function(){
            var pageHeight = this.getPageHeight();
            var scrollHeight = this.getScrollHeight();
            var bottomHeight = this.getFooterHeight('guoku_footer');
            console.log(bottomHeight);
            var bottomHeight = this.getFooterHeight('guoku_footer') + 50;
            console.log(bottomHeight);
        },
        getScrollHeight:function(){
            return document.body.scrollTop;
        },
        getPageHeight:function(){
            return document.body.scrollHeight;
        },
        getFooterHeight:function(id){
            return document.getElementById(id).offsetHeight;
        }
    });
    return AnnualReport;
});



