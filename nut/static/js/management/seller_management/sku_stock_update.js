var SKUStockUpdateManager = Class.extend({
    init: function(){
        console.log('init sku stock ,margin and price update begin');
        this.initEditPencil();
        this.initSaveBtn();
    },
    initEditPencil:function(){
        $('.sku-edit-pencil').click(this.showInputContent.bind(this));
    },
    showInputContent:function(event){
        $(event.currentTarget).parent().addClass('hidden');
        $(event.currentTarget).parent().next().addClass('show');
    },
    initSaveBtn:function(){
        $('.sku-save-btn').click(this.postUpdateSku.bind(this));
    },
    postUpdateSku:function(event){
        var that = this;
        var targetElement = $(event.currentTarget);
        var targetInput = targetElement.prev();
        var url =  targetElement.attr('data-url');
        //var entity_id = targetInput.attr('data-entity-id');
        var sku_id = targetInput.attr('data-sku-id');
         var inputValue =  targetInput.val();
        var price,stock,data,margin;

        if(targetInput.parent().hasClass('price-edit-wrapper')){

            price = inputValue;
            data = {
            'sku_id':sku_id,
            'price':price
            };

        }else if(targetInput.parent().hasClass('margin-edit-wrapper')){
           margin = inputValue;
           data = {
               'sku_id' : sku_id,
               'margin': margin
           };
        }
        else{

            stock = inputValue;
            data = {
            'sku_id':sku_id,
            'stock':stock
            };

        }

        $.when($.ajax({

            url:url,
            method:'POST',
            data:data

            })).then(
            that.postSaveSuccess.bind(this),
            that.postSaveFail.bind(this)
        );
    },
    postSaveSuccess:function(data){
        var that = this;
        var status = parseInt(data.status);
        if(status > 0){
            bootbox.alert({
                size: 'small',
                message: '更新成功!',
                callback:that.reloadCurrentPage()
            }) ;
        }
    },
    postSaveFail:function(data){
        var that = this;
        bootbox.alert({
            size: 'small',
            message: '更新失败!',
            callback:that.reloadCurrentPage()
        }) ;
    },
    reloadCurrentPage:function(){
        window.setTimeout( function(){ window.location.reload();}, 2000);
    }
});


(function($, window, document){
    $(function(){
        var sku_stock_update_manager = new SKUStockUpdateManager();
    });
})(jQuery, window, document);
