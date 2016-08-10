var SKUEditManager = Class.extend({
    init: function(){
        console.log('sku edit begin');
        this.initSkuEdit();
    },
    initSkuEdit:function(){
        var that = this;
        $('.edit-sku-trigger').click(function(){
            var url = $(this).attr('data-url');
            $.when($.ajax({
                url: url,
                method: 'GET'
            })).then(
                function(html){
                    bootbox.dialog({
                        message: html
                    });
                    //成功渲染弹框之后再初始化保存按钮
                    that.initSaveSku();
                },
                function(){
                    console.log('get form fail ');
                });
        });
    },
    post_edit_sku: function(){
        var that = this;
        var _form = $('#sku_form');
        _form.onsubmit=function(){return false;};
        alert(_form.serialize());

        $.when($.ajax({
            url: _form.attr('action'),
            method: 'POST',
            data: _form.serialize()
        })).then(
            that.post_edit_sku_success.bind(this),
            that.post_edit_sku_fail.bind(this)
        );
    },
    post_edit_sku_success: function editSkuSuccess(data){
        var that = this;
        this.hideDialog();
         var status = parseInt(data.status);
        if(status == 1){
            bootbox.alert({
                size: 'small',
                message: '添加成功!',
                callback: that.reloadCurrentPage()
            }) ;
        }
        else if(status == -1){
             bootbox.alert({
                size: 'small',
                message: '添加重复,请重新添加!'
            }) ;
        }
        else{
            return bootbox.alert({
                size: 'small',
                message: '添加失败'
            }) ;
        }
    },
    post_edit_sku_fail:function(data){
        this.hideDialog();
        console.log('post edit sku fail');
    },

    initSaveSku:function(){
        $('.sku-save').click(this.post_edit_sku.bind(this));
    },
     hideDialog:function(){
           bootbox.hideAll();
     },
    reloadCurrentPage:function(){
        window.location.reload();
    }

});


(function($, window, document){
    $(function(){
        var sku_manager = new SKUEditManager();
    });
})(jQuery, window, document);
