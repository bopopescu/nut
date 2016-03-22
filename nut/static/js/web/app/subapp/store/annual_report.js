
define(['jquery', 'libs/Class','libs/slick'], function(
    $, Class
){
    var AnnualReport= Class.extend({
        init: function () {
            console.log('hello rose.write codes here');
            if(this.getScrollHeight() > this.getPageHeight() - this.getFooterHeight('guoku_footer') - 50 ){
                console.log('hide');
                this.hideReport();
            }else{
                console.log('show');
            }

        },
        hideReport:function(){
            var report = document.getElementById(id);
            $(report).hide();
        },
        getScrollHeight:function(){
            return $(window).scrollTop;
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



