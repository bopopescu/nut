define(function(require){

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

        }

    });

    return applicationController;

});