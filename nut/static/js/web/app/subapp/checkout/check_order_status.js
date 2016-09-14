var CheckoutManager = Class.extend({
    init: function(){
        this.initCheckOrderStatusBtn();
        this.dialog_html = $('#checkdesk_payment_input').html();
    },
    initCheckOrderStatusBtn:function(){
        $('.btn.order-pay-button').click(this.showDialog.bind(this));
    },
    showDialog:function(event){
        var target = event.currentTarget;
        this.url = $(target).attr('data-url');
        this.order_id = $(target).attr('data-order-id');

        bootbox.dialog({
            title: '付款方式选择',
            message : this.dialog_html,
            buttons:{
                success:{
                    label: '确定付款',
                    className: 'btn-success',
                    callback: this.setOrderPaid.bind(this)
                },
                giveup: {
                    label: '放弃付款',
                    className: 'btn-fail',
                    callback: this.giveupPayment.bind(this)
                }
            }

        });
        //bootbox.confirm("确认已经成功收到买家付款?",function(result){
        //    if(result){
        //        that.setOrderPaid(url,order);
        //
        //    }else{
        //        return ;
        //    }
        //});
    },
    giveupPayment: function(){
        bootbox.hideAll();
    },

    get_payment_type: function(){
        return $('input[name="payment_type"]:checked').val();
    },

    get_payment_note:function(){
        return $('#payment_note').val();
    },

    setOrderPaid:function(){
        var that = this;
        $.when($.ajax({
            url: this.url,
            method: 'POST',
            data: {
                'order_id':this.order_id,
                'payment_type': this.get_payment_type(),
                'payment_note': this.get_payment_note()
            }
        })).then(
            that.paySuccess.bind(this),
            that.payFail.bind(this)
        );

    },

    paySuccess:function(data){
        var that = this;
        var res = parseInt(data.result);
        if(res == 1){
            bootbox.alert({
                size: 'small',
                message: '操作成功!',
                callback:that.reloadCurrentPage()
            }) ;
        }
    },
    payFail:function(data){
        console.log('post fail');
        var that = this;
        var res = parseInt(data.responseJSON.result);
        if(res == 0){
            bootbox.alert({
                size: 'small',
                message: data.responseJSON.message,
                callback:that.reloadCurrentPage()
            }) ;
        }
    },
    reloadCurrentPage:function(){
         window.setTimeout( function(){ window.location.reload();}, 2000);
    }

});

(function($, window, document){
    $(function(){
         var checkout_manager = new CheckoutManager();
    });
})(jQuery, window, document);

