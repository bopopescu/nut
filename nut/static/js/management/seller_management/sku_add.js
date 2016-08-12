var SKUAddManager = Class.extend({
    init: function(){
        console.log('sku add begin');
        this.initSkuAdd();

    },
    show_sku_add_dialog: function(e){
            var that = this ;
            var target = e.currentTarget;
            var url = $(target).attr('data-url');
            console.log('get add sku model url');
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
    },

    initSkuAdd:function(){
        var that = this;
        $('#add_sku_trigger').click(this.show_sku_add_dialog.bind(this));
    },
    post_add_sku: function(){
        var that = this;
        var _form = $('#sku_form');
        _form.find('#id_attrs').val(this.sku_attr_app.collect_attribute());
        _form.onsubmit=function(){return false;};
        //alert(_form.serialize());

        $.when($.ajax({
            url: _form.attr('action'),
            method: 'POST',
            data: _form.serialize(),
            dataType:'json'
        })).then(
            that.post_add_sku_success.bind(this),
            that.post_add_sku_fail.bind(this)
        );
    },
    post_add_sku_success: function addSkuSuccess(data){
        var that = this;
        this.hideDialog();
         var success_status = parseInt(data.result);
        if(success_status == 1){
            bootbox.alert({
                size: 'small',
                message: '添加成功!',
                callback:that.reloadCurrentPage()
            }) ;
        }
    },
    post_add_sku_fail:function(data){
        this.hideDialog();
        console.log('post add sku fail');
        var fail_status = parseInt(data.responseJSON.result);
        console.log('status'+fail_status);

        if(fail_status == -1){
             bootbox.alert({
                size: 'small',
                message: '商品属性重复,请重新添加!'
            }) ;
        }
        else{
            return bootbox.alert({
                size: 'small',
                message: '添加失败'
            }) ;
        }
    },

    initSaveSku:function(){
        $('.sku-save').click(this.post_add_sku.bind(this));
        this.sku_attr_app = new SKU_MNG_APP();
    },
     hideDialog:function(){
           bootbox.hideAll();
     },
    reloadCurrentPage:function(){
         window.setTimeout( function(){ window.location.reload();}, 2000);
    }

});


(function($, window, document){
    $(function(){
        var sku_manager = new SKUAddManager();
    });
})(jQuery, window, document);
