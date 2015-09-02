define(function (require) {

    "use strict";
    if (!GlobalControllerName){
        alert('can not find GlobalControllerName');
    }
    var APPController = require(GlobalControllerName);
    return Backbone.Router.extend({
        initialize: function(){
             window.APP =  new APPController();
        }
    });

});