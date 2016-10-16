var OfflineShopManager = Class.extend({
    init: function(){
        console.log('offline shop begin');
        this.initAddPicBtn();
    },

    initAddPicBtn:function(){
        $('#add_pic_button').click(this.show_add_pic_dialog.bind(this));
    },
     show_add_pic_dialog:function(e){
           bootbox.alert('show add pic dialog');
        }

});


(function($, window, document){
    $(function(){
        var sku_manager = new OfflineShopManager();
    });
})(jQuery, window, document);
