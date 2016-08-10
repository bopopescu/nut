var SKUAddManager = Class.extend({
    init: function(){
        console.log('sku add begin');
        this.initSkuAdd();
    },
    initSkuAdd:function(){
        var that = this;
        $('#add_sku_trigger').click(function(){
            var url = $(this).attr('data-url');
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
        });
    },
    post_add_sku: function(){
        var that = this;
        var _form = $('#sku_form');
        _form.onsubmit=function(){return false;};

        $.when($.ajax({
            url: _form.attr('action'),
            method: 'POST',
            data: _form.serialize()
        })).then(
            that.post_add_sku_success.bind(this),
            that.post_add_sku_fail.bind(this)
        );
    },
    post_add_sku_success: function addSkuSuccess(data){
        //var that = this;
        this.hideDialog();
         var status = parseInt(data.status);
        if(status == 1){
            bootbox.alert({
                size: 'small',
                message: '添加成功!'
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
    post_add_sku_fail:function(data){
        this.hideDialog();
        console.log('post add sku fail');
    },

    initSaveSku:function(){
        $('.sku-save').click(this.post_add_sku.bind(this));
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
        var sku_manager = new SKUAddManager();
    });
})(jQuery, window, document);
