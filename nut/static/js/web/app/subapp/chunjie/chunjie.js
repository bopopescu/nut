define(['libs/Class'], function(
    Class
){

    var ChunjieApp = Class.extend({
        init: function(){
            console.log('chunjieApp init');
            this.configWX();
            wx.ready(function(){
                alert('wx ready');
            });

        },
        configWX: function(){
            wx.config({
                debug: true,
                appId: signature_obj.appid,
                timestamp: signature_obj.timestamp,
                nonceStr : signature_obj.noncestr,
                signature : signature_obj.signature,
                jsApiList: ['onMenuShareTimeline',
                            'onMenuShareAppMessage',
                            'onMenuShareWeibo',
                            'hideOptionMenu',
                            'showOptionMenu'
                ]

            });
        },
    });

    return ChunjieApp;
});