define(function (require) {

    "use strict";

    var APPController = require("controllers/flinkApplicationController");
    return Backbone.Router.extend({
        initialize: function(){
             window.APP =  new APPController();
        }
    });

});