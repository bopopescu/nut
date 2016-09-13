var PrintCheckedEntityManager = Class.extend({
    init: function(){
        console.log('print checked entity begin');
        this.initPrintQRCodeBtn();
    },
    initPrintQRCodeBtn:function(){
        console.log('init print btn');

    }

});

(function($, window, document){
    $(function(){
        var print_checked_entity_manager = new PrintCheckedEntityManager();
    });
})(jQuery, window, document);
