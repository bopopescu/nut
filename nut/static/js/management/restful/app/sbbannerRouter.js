define(function (require) {

    "use strict";

    var APPController = require("controllers/sbbannerApplicationController");
    return Backbone.Router.extend({
        initialize: function(){
             window.APP =  new APPController();
        }
    });

});