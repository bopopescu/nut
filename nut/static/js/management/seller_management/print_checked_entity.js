var PrintCheckedEntityManager = Class.extend({
    init: function(){
        console.log('print checked entity begin');
        this.initPrintQRCodeBtn();
    },
    initPrintQRCodeBtn:function(){
        console.log('init print btn');
        $('#checked_print_qrcode').click(this.handlePrintQrcode.bind(this));
    },
    handlePrintQrcode:function(e) {
        var checked_entity_ids = this.collectCheckedEntity();
        var print_count_list = this.collectPrintCounts();
        if(checked_entity_ids.length){
            var new_url = 'qrcode_list?entity_ids=' +  JSON.stringify(checked_entity_ids) + '&print_counts=' + JSON.stringify(print_count_list);
            window.open(new_url);
        }else{
            window.open('qrcode_list');
        }
    },
    collectCheckedEntity:function(){
         var checked_entity_collection = $('.usite-chk:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        return [].slice.call(checked_entity_collection);
    },
     collectPrintCounts:function(){
         var print_count_collection = $('.print-count').map(function(idx, item){
            return $(item).attr('value');
        });
        return [].slice.call(print_count_collection);
    }
});

(function($, window, document){
    $(function(){
        var print_checked_entity_manager = new PrintCheckedEntityManager();
    });
})(jQuery, window, document);
