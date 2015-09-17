define(function(require){

    var FLink = require('models/FLink').FLink;
    var FLinkCollection = require('models/FLink').FLinkCollection;
    var FLinkListView = require('views/flink');


    var applicationController = function(){
        if(this.initialize && _.isFunction(this.initialize)){
            this.initialize.apply(this, [].slice.call(arguments));
        }
    };
    _.extend(applicationController.prototype , {
        initialize: function(){

            this.flinkCollection = new FLinkCollection();
            var flinkListView = new FLinkListView({
                el: '#FLink-management',
                collection: this.flinkCollection
            });
        }

    });
    return applicationController;

});