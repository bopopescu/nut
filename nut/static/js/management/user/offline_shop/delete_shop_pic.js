var DeleteShopPicManager = Class.extend({
    init: function(){
        console.log('delete shop pic begin');
        this.initDetelePicBtn();
    },
    initDetelePicBtn:function(){
         $('.btn.delete-pic-btn').click(this.sendDeletePicAjax.bind(this));

    },
    sendDeletePicAjax:function(e){
        var target_url = $(e.currentTarget).attr("data-url");
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

});


(function($, window, document){
    $(function(){
         var sku_manager = new DeleteShopPicManager();
    });
})(jQuery, window, document);