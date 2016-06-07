
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
            this.initClickBell();
        },
        initClickBell: function(){
            var flag = 0;
            var that = this;
                 $('.navbar-collapse .notification-icon').click(function(){
                    $('.navbar-collapse .notification-drop-list-wrapper').toggle(flag++ % 2 == 0);
                     console.log('flag:'+flag);

                 });


        },
        //showNotificationDropList:function(){
        //    var that = this;
        //     $('.navbar-collapse .notification-drop-list-wrapper').toggle(that.flag++ % 2 == 0);
        //
        //}
        //hiddenNotificationDropList:function(){
        //     $('.navbar-collapse .notification-drop-list-wrapper').hide();
        //     this.flag = false;
        //     console.log('flag:'+this.flag);
        //},
        //postAjaxNotification:function(){
        //    console.log('post ajax request');
        //     $.when(
        //            $.ajax({
        //                cache:true,
        //                type:"post",
        //                url: '',
        //                data:''
        //            })
        //        ).then(
        //          this.postSuccess.bind(this),
        //         this.postFail.bind(this)
        //        );
        //},
        //postSuccess:function(result){
        //    var status = parseInt(result.status);
        //    if(status == 1){
        //        this.showNotificationItems();
        //    }else{
        //        this.showFail();
        //    }
        //},
        //showNotificationItems:function($ele){
        //    var ajaxDatas = $ele;
        //    var notificationItems = _.template($('#notification_item_template').html());
        //    var datas = {
        //        name:ajaxDatas['name'],
        //        name:ajaxDatas['name']
        //    };
        //    $('.notification-drop-list').append(notificationItems(datas));
        //},
        //postFail:function(){
        //    console.log('request failed.please try again');
        //}

    });

    return TopNotification;
});