define(['jquery',
        'bootbox',
        'libs/Class'
    ],
    function(
    $,
    bootbox,
    Class
){

    var EntityReport = Class.extend({
        init: function(){
             var that  = this ;
             $('#report_trigger').click(function(){
                    var url = $(this).attr('report-url');
                    $.when($.ajax({
                        url: url,
                        method: 'GET',
                    })).then(
                        function(htmltext){
                            //this call will return a  rendered template
                            bootbox.dialog({
                               title: '举报商品',
                               message: htmltext,
                                buttons: {
                                    success:{
                                        label:'发送',
                                        className:'btn-primary',
                                        callback: that.sendReport.bind(that)
                                    },
                                }
                            });
                        },function(){
                            console.log('get report form fail ');
                        });
                });
        },
        sendReport: function(){
            var _form = $('#report_form_wrapper form');
                if (_form.length){
                    $.when($.ajax({
                        url: _form.attr('action'),
                        data: _form.serialize(),
                        method: 'POST',
                    })).then(
                        function reportSuccess(data){
                            return bootbox.alert({
                                size: 'small',
                                message: '举报发送成功，感谢您的关心。'
                            }) ;
                        },
                        function reportFail(){
                            return ;
                        }
                    );
                }
            }


    });

        return EntityReport;

});