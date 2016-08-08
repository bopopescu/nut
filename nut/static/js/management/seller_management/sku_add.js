var SKUAddManager = Class.extend({
    init: function(){
        console.log('sku add begin');
        this.initSkuAdd();
    },
    initSkuAdd:function(){
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
                        title: '添加规格',
                        message: html,
                        buttons: {
                            success:{
                                label:'保存',
                                className:'btn newest-btn-primary',
                                callback: function(){
                                    var _form = $('#sku_add_form');
                                    if (_form.length){
                                        $.when($.ajax({
                                            url: _form.attr('action'),
                                            method: 'POST'
                                        })).then(
                                                function addSkuSuccess(data){
                                                    if(data == 1){
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
                                    }
                                }
                            }
                        }
                    });
                },function(){
                    console.log('get form fail ');
                });
    });
    }

});


(function($, window, document){
    $(function(){
         var sku_manager = new SKUAddManager();
    });
})(jQuery, window, document);
