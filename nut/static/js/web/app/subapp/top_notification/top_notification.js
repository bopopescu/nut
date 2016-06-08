
define([
    'libs/Class',
    'jquery',
    'libs/fastdom',
    'underscore',
     'cookie'
], function(
    Class,
    $,
    fastdom,
    _
){


    var TopNotification = Class.extend({
        init: function(){
            this.flag = 0;
            console.log('top notification begin');
            this.initClickBell();
        },
        initClickBell: function(){
            $('.navbar-collapse .notification-icon').click(this.handleClickBell.bind(this));
        },
        handleClickBell:function(){
            $('.navbar-collapse .notification-drop-list-wrapper').toggle(this.flag++ % 2 == 0);
            console.log('flag:'+this.flag);
            if(this.flag % 2 == 0){
                console.log('no request');
            }else{
                this.postAjaxNotification();
            }
        },
        postAjaxNotification:function(){
            console.log('post ajax request');
             $.when(
                    $.ajax({
                        cache:true,
                        type:"get",
                        url: '/message/newmessage/',
                        data:''
                    })
                ).then(
                  this.postSuccess.bind(this),
                 this.postFail.bind(this)
                );
        },
        postSuccess:function(result){
            var status = parseInt(result.status);
            //alert(result.data[0].type);
            if(status == 1){
                alert(result.data.length);
                alert(result.data[0].type);
                 alert(result.data[0].actor.nick);
                this.showNotificationItems();
            }else{
                this.showFail();
            }
        },
        showNotificationItems:function($ele){
            var ajaxDatas = $ele;
            var notificationItems = _.template($('#notification_item_template').html());
            //var datas = {
            //    type:ajaxDatas[0].type,
            //    name:ajaxDatas[0].actor.id
            //};
            //$('.notification-drop-list').append(notificationItems(datas));
        },
        postFail:function(){
            console.log('request failed.please try again');
        }

    });

    return TopNotification;
});