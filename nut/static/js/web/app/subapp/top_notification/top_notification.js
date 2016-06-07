
define(['libs/Class', 'jquery','cookie'], function(Class, $){


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
             this.flag = true;
             console.log('flag:'+this.flag);
        },
        hiddenNotificationDropList:function(){
             $('.navbar-collapse .notification-drop-list-wrapper').hide();
             this.flag = false;
             console.log('flag:'+this.flag);
        }

    });

    return TopNotification;
});