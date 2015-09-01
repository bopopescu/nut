define(function(require){

    var SBBanner = require('models/SBBanner').SBBanner;
    var SBBannerCollection = require('models/SBBanner').SBBannerCollection;
    var SBBannerListView = require('views/sbbanner')


    var applicationController = function(){
        if(this.initialize && _.isFunction(this.initialize)){
            this.initialize.apply(this, [].slice.call(arguments));
        }
    };
    _.extend(applicationController.prototype , {
        initialize: function(){

            this.sbbannerCollection = new SBBannerCollection();
            var sbbannerList = new SBBannerListView({
                el: '#SBBanner-management',
                collection: this.sbbannerCollection,
            });
        }

    });
    return applicationController;

});