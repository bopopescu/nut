define(['Backbone', 'libs/Class'],function(Backbone, Class){

    var EntityModel = Backbone.Model.extend({
        urlRoot: '/api/webentity/',
        getLikeUserCollection : function(){
            try {
                return this.get('limited_likers.results');
            }
            catch(e){
                return [];
            }

        },
        parse: function(data){
            return data;
        },

    });

    return EntityModel;


});