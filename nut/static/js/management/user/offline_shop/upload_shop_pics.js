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
            title: '上传图片',
            onEscape: true,
            backdrop:true,
            closeButton: true,
            animate: true,
            className: 'upload-pic-dialog',
            message:this.upload_pic_modal_content
        });
        this.initFileUploadBtn();
    },
    initFileUploadBtn:function(){
        $('#file_upload_btn').click(this.sendFile(this.handleUploadSuccess(url)));
    },
    sendFile:function(callback){
        callback = callback || function(){};
        var file = document.getElementById('file_image').files;
        var  data = new FormData();
        data.append("file", file[0]);
        //console.log('file:'+file);
         $.ajax({
                data: data,
                type: "POST",
                url: "/management/media/upload/image/",
                cache: false,
                contentType: false,
                processData: false,
                success: function(url) {
                    callback(url);
                    //bootbox.hideAll();
                    //bootbox.alert('上传成功');
                    window.setTimeout(function(){
                        bootbox.hideAll();
                    }, 1000);
                },
                error: function(data){
                    bootbox.hideAll();
                    bootbox.alert('上传失败， 请稍后再试');
                    //console.log(data);
                    //console.log('FILE UPLOAD FAIL');
                }
            });
    },
    handleUploadSuccess:function(url){
        console.log('upload success');
    }
});


(function($, window, document){
    $(function(){
        var offline_shop_manager = new OfflineShopManager();
    });
})(jQuery, window, document);
