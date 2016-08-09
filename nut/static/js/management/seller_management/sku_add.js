var SKUAddManager = Class.extend({
    init: function(){
        console.log('sku add begin');
        this.initSkuAdd();
        //this.initSaveSku();
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
                    //will return a  rendered template
                    bootbox.dialog({
                        title: '添加SKU',
                        message: html,
                        //buttons: {
                        //    success:{
                        //        label:'发送',
                        //        className:'btn newest-btn-primary',
                                //callback: function(){
                                //    var _form = $('#sku_add_form');
                                //    if (_form.length){
                                //        $.when($.ajax({
                                //            url: _form.attr('action'),
                                //            method: 'POST'
                                //        })).then(
                                //                function addSkuSuccess(data){
                                //                    if(data){
                                //                         return bootbox.alert({
                                //                        size: 'small',
                                //                        message: '添加成功'
                                //                    }) ;
                                //                    }else{
                                //                       return bootbox.alert({
                                //                        size: 'small',
                                //                        message: '添加失败'
                                //                    }) ;
                                //                    }
                                //                }
                                //        );
                                //    }
                                //}
                        //    }
                        //}
                    });
                    //成功渲染弹框之后再初始化保存按钮
                    that.initSaveSku();
                },function(){
                    console.log('get form fail ');
                });
    });
    },
    initSaveSku:function(){
        $('.sku-save').click(function(){
             var _form = $('#sku_add_form');
            $.when($.ajax({
                url: _form.attr('action'),
                method: 'POST'
            })).then(
                function addSkuSuccess(data){
                    if(data){
                        return bootbox.alert({
                            size: 'small',
                            message: '添加成功'
                        }) ;
                    }else{
                        return bootbox.alert({
                            size: 'small',
                            message: '添加失败'
                        }) ;
                    }
                }
            );
        })
    }

});


(function($, window, document){
    $(function(){
         var sku_manager = new SKUAddManager();
    });
})(jQuery, window, document);
