var OfflineShopManager = Class.extend({
    init: function(){
        console.log('offline shop begin');
        this.initAddPicBtn();
        this.upload_pic_modal_content = $('#add_pic_modal_content').html();
    },

    initAddPicBtn:function(){
        $('#add_pic_button').click(this.show_add_pic_dialog.bind(this));
    },
    show_add_pic_dialog:function(e){
        bootbox.hideAll();
        bootbox.dialog({
            title: '上传商店图片',
            onEscape: true,
            backdrop:true,
            closeButton: true,
            animate: true,
            className: 'upload-pic-dialog',
            message:this.upload_pic_modal_content
        });

    }

});


(function($, window, document){
    $(function(){
        var sku_manager = new OfflineShopManager();
    });
})(jQuery, window, document);
