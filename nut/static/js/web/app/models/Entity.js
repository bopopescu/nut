define(['Backbone', 'libs/Class'],function(Backbone, Class){

    var EntityModel = Backbone.Model.extend({
        urlRoot: '/api/webentity/',
        getLikerCollection : function(){
            throw('not implemented');
        },
        parse: function(data){
            console.log(data);
        },

    });

    return EntityModel;


});