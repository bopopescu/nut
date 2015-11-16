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
                                        callback: sendReport
                                    },
                                }
                            });
                        },function(){
                            console.log('get report form fail ');
                        });
                });
        }
    });

        return EntityReport;

});