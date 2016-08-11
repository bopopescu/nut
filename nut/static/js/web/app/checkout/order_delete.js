var ORDERManager = Class.extend({
    init: function(){

        $('.btn.order-delete-trigger').on('click', delete_order);
        function delete_order(e) {
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
         var order_manager = new ORDERManager();
    });
})(jQuery, window, document);

