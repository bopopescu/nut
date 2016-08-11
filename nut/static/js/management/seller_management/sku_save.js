var SKUManager = Class.extend({
    init: function(){
        // var that = this ;
        $('.btn.newest-btn-primary').on('click', update_sku);
        function update_sku(e) {
                e.preventDefault();
                $(this).off('click');
                var sku_id = $(this).attr("id");
                var price = $("input#" + sku_id +"_price").val();
                var stock = $("input#" + sku_id +"_stock").val();
                bootbox.confirm('确定要保存修改吗？', function(result){
                    if(result){
                        $.ajax({
                        url: '/seller_management/sku_save/',
                        method: 'POST',
                        data:{
                            'id':JSON.stringify(sku_id),
                            'price':JSON.stringify(price),
                            'stock':JSON.stringify(stock)
                        }
                        }).done(function() {
                            console.log('save success');
                        });

                }else{
                    return ;
                }
            });

        }

    },

});


(function($, window, document){
    $(function(){
         var sku_manager = new SKUManager();
    });
})(jQuery, window, document);

