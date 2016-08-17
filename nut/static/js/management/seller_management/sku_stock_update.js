var SKUStockUpdateManager = Class.extend({
    init: function(){
        console.log('init sku stock update begin');
        this.initEditPencil();
        this.initSaveBtn();
    },
    initEditPencil:function(){
        $('.stock-edit-pencil').click(this.showInputContent.bind(this));
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
        var stock =  targetInput.val();

        var data = {
            'sku_id':sku_id,
            'stock':stock
        };

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
        if(data.status > 0){
             bootbox.alert('更新成功');
        }
    },
    postSaveFail:function(data){
         bootbox.alert('更新失败');
    }
});


(function($, window, document){
    $(function(){
        var sku_stock_update_manager = new SKUStockUpdateManager();
    });
})(jQuery, window, document);
