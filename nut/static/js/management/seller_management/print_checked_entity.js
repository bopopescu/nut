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
        var new_url = 'seller_management/qrcode_list/?entity_ids=' +  JSON.stringify(checked_entity_ids)
        window.open('new_url')

        var url = $(e.currentTarget).attr('data-url');
        if(checked_entity_ids){
            console.log('checked entities');
        }

        this.postPrintQrcode(checked_entity_ids,url);
    }
    ,
    collectCheckedEntity:function(){
         var checked_entity_collection = $('.usite-chk:checked').map(function(idx, item){
            return $(item).attr('value');
        });
        return [].slice.call(checked_entity_collection);
    },
    postPrintQrcode:function(entities,url){
         $.when($.ajax({
            url: url,
            method: 'POST',
            data:{'checked_entity_ids':JSON.stringify(entities)}
        })).then(
            this.checkedPrintEntitySuccess.bind(this),
            this.checkedPrintEntityFail.bind(this)
        );
    },
    checkedPrintEntitySuccess:function(){
        console.log('checked print entity success');
        //var target_url = $('#checked_print_qrcode').attr('data-url');
        //window.location.href = window.location.host + target_url;
    },
    checkedPrintEntityFail:function(){
        console.log('checked print entity fail');
    }
});

(function($, window, document){
    $(function(){
        var print_checked_entity_manager = new PrintCheckedEntityManager();
    });
})(jQuery, window, document);
