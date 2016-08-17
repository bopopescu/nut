var SKUStockUpdateManager = Class.extend({
    init: function(){
        console.log('init sku stock update begin');
        this.initEditPencil();
    },
    initEditPencil:function(){
        $('.stock-edit-pencil').click(this.showInputContent.bind(this));
    },
    showInputContent:function(event){
        $(event.currentTarget).parent().addClass('hidden');
        $(event.currentTarget).parent().next().addClass('show');
    }

});


(function($, window, document){
    $(function(){
        var sku_stock_update_manager = new SKUStockUpdateManager();
    });
})(jQuery, window, document);
