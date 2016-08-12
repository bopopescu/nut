var SKUEditManager = Class.extend({
    init: function(){
        console.log('sku edit begin');
        this.initSkuEdit();
    },
    show_sku_edit_dialog:function(e){
            var that = this;
            var target = e.currentTarget;
            var url = $(target).attr('data-url');
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
                    that.sku_attr_app = new SKU_MNG_APP();
                    //that.sku_attr_app.render_attributes();
                    if($('#sku_form').find('input')){
                        return ;
                    }else{
                      that.sku_attr_app.render_attributes();
                    }

                },
                function(){
                    console.log('get form fail ');
                });
        },
    initSkuEdit:function(){
        $('.edit-sku-trigger').click(this.show_sku_edit_dialog.bind(this));
    },
    post_edit_sku: function(){
        var that = this;
        var _form = $('#sku_form');
        _form.find('#id_attrs').val(this.sku_attr_app.collect_attribute());
        _form.onsubmit=function(){return false;};
        //alert(_form.serialize());

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
         var success_status = parseInt(data.result);
        if(success_status == 1){
            bootbox.alert({
                size: 'small',
                message: '编辑成功!',
                callback:that.reloadCurrentPage()
            }) ;
        }
    },
    post_edit_sku_fail:function(data){
        this.hideDialog();
        console.log('post add sku fail');
        var fail_status = parseInt(data.responseJSON.result);

        if(fail_status == -1){
             bootbox.alert({
                size: 'small',
                message: '商品属性重复,请重新编辑!'
            }) ;
        }
        else{
            return bootbox.alert({
                size: 'small',
                message: '编辑失败!'
            }) ;
        }
    },

    initSaveSku:function(){
        $('.sku-save').click(this.post_edit_sku.bind(this));
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
        var sku_manager = new SKUEditManager();
    });
})(jQuery, window, document);
