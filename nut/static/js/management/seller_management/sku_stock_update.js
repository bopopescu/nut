var SKUStockUpdateManager = Class.extend({
    init: function(){
        console.log('init sku stock update begin');
    }

});


(function($, window, document){
    $(function(){
        var sku_stock_update_manager = new SKUStockUpdateManager();
    });
})(jQuery, window, document);
