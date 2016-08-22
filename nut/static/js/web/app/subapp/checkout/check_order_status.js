var CheckoutManager = Class.extend({
    init: function(){
        this.initCheckOrderStatusBtn();
    },
    initCheckOrderStatusBtn:function(){
        $('.btn.check-order-status').click(this.showDialog.bind(this));
    },
    showDialog:function(event){
        var that = this;
        var target = event.currentTarget;
        var url = $(target).attr('data-url');
        var order = $(target).attr('data-order-id');

        bootbox.confirm("确认已经成功收到买家付款?",function(result){
            if(result){
                that.postUpdateOrderStatus(url,order);

            }else{
                return ;
            }
        });
    },
    postUpdateOrderStatus:function(url,order){
        var that = this;
        $.when($.ajax({
            url: url,
            method: 'POST',
            data: {
                'order_id':order
            }
        })).then(
            that.postSuccess.bind(this),
            that.postFail.bind(this)
        );

    },
    postSuccess:function(data){
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
    postFail:function(data){
        console.log('post fail');
        var that = this;
        var res = parseInt(data.responseJSON.result);
        if(res == 0){
            bootbox.alert({
                size: 'small',
                message: '操作失败!请稍后重新尝试!',
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

