define(['libs/Class'], function(
    Class
){

    var ChunjieApp = Class.extend({
        init: function(){
            console.log('chunjieApp init');
            this.configWX();

        },
        configWX: function(){
            wx.config({
                debug: true,
                appId:'guokuapp',


            });
        },
    });

    return ChunjieApp;
});