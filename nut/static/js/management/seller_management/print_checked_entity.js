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
        if(checked_entity_ids.length){
            var new_url = 'qrcode_list?entity_ids=' +  JSON.stringify(checked_entity_ids);
            window.open = new_url;
        }else{
            window.location.href = 'qrcode_list';
        }
    },
    collectCheckedEntity:function(){
         var checked_entity_collection = $('.usite-chk:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        return [].slice.call(checked_entity_collection);
    }
});

(function($, window, document){
    $(function(){
        var print_checked_entity_manager = new PrintCheckedEntityManager();
    });
})(jQuery, window, document);
