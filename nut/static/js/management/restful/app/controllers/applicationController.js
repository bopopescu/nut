define(function(require){
    var SBBanner = require('models/SBBanner').SBBanner;
    var SBBannerCollection = require('models/SBBanner').SBBannerCollection;


    var applicationController = function(){
        if(this.initialize && _.isFunction(this.initialize)){
            this.initialize.apply(this, [].slice.call(arguments));
        }
    };
    _.extend(applicationController.prototype , {
        initialize: function(){
            console.log('in application controller');
            console.log('backBone');
            console.log(Backbone);
            sbbanners = new SBBannerCollection();
            sbbanners.fetch();
            window.sbbanners = sbbanners;
        }

    });

    return applicationController;

});