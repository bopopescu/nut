var SKUManager = Class.extend({
    init: function(){

        $('.btn.sku-delete-trigger').on('click', delete_sku);
        function delete_sku(e) {
                e.preventDefault();
                $(this).off('click');
                var target_url = $(this).attr("data-url");
                bootbox.confirm('确定要删除吗？', function(result){
                    if(result){
                        $.ajax({
                        url: target_url,
                        method: 'POST',
                        data:{

                        }
                        }).done(function() {
                           bootbox.alert({
                               size: 'small',
                               message: '删除成功'
                           }) ;
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

