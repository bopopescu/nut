define(function (require) {

    "use strict";

    var APPController = require("controllers/articleApplicationController");
    return Backbone.Router.extend({
        initialize: function(){
             window.APP =  new APPController();
        },
        routes:{
            'selection_published':'sla_pub',
            'selection_pending':'sla_pending',
            'edit/:id': 'edit_article',
        },
        sla_pub: function(){
            console.log('selection pubed ');
        },
        sla_pending:function(){
            console.log('selection poending');
        },
        edit_article: function(id){
            console.log(id);
        },
    });

});