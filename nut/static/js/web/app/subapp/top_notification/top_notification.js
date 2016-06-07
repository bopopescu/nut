
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
            console.log('top notification begin');
            this.flag = false;
            console.log('flag:'+this.flag);
            this.initClickBell();
        },
        initClickBell: function(){
            if(!this.flag){
                 $('.navbar-collapse .notification-icon').click(this.showNotificationDropList.bind(this));
            }else{
                 $('.navbar-collapse .notification-icon').click(this.hiddenNotificationDropList.bind(this));
            }

        },
        showNotificationDropList:function(){
             $('.navbar-collapse .notification-drop-list-wrapper').show();
             this.postAjaxNotification();
             this.flag = true;
             console.log('flag:'+this.flag);

        },
        hiddenNotificationDropList:function(){
             $('.navbar-collapse .notification-drop-list-wrapper').hide();
             this.flag = false;
             console.log('flag:'+this.flag);
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
            if(status == 1){
                this.showNotificationItems();
            }else{
                this.showFail();
            }
        },
        showNotificationItems:function($ele){
            var ajaxDatas = $ele;
            var notificationItems = _.template($('#notification_item_template').html());
            var datas = {
                name:ajaxDatas['name'],
                name:ajaxDatas['name']
            };
            $('.notification-drop-list').append(notificationItems(datas));
        },
        postFail:function(){
            console.log('request failed.please try again');
        }

    });

    return TopNotification;
});