var CheckoutManager = Class.extend({
    init: function(){
        console.log('checkout begin');

        $('.btn.check-order-status').on('click', check_order_status);
        function check_order_status(e) {
                e.preventDefault();
                $(this).off('click');
                var target_url = $(this).attr("data-url");
                var order_id = $(this).attr("data-order-id");
                bootbox.confirm('确认已经成功收到买家付款？', function(result){
                    if(result){
                        $.ajax({
                        url: target_url,
                        method: 'POST',
                        data:{
                            order_id:order_id

                        }
                        }).done(function() {
                           bootbox.alert({
                               size: 'small',
                               message: '操作成功'
                           }) ;

                            window.setTimeout( function(){ bootbox.hideAll();}, 1000);
                            window.location.reload();
                        });

                    }else{
                       return ;
                    }
            });

        }

    }
});


(function($, window, document){
    $(function(){
         var checkout_manager = new CheckoutManager();
    });
})(jQuery, window, document);

