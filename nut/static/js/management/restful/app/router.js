define(function (require) {

    "use strict";

    var APPController = require("controllers/applicationController");
    return Backbone.Router.extend({
        initialize: function(){
             window.APP =  new APPController();
        }
    });

});