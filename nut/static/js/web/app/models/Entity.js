define(['Backbone', 'libs/Class'],function(Backbone, Class){

    var EntityModel = Backbone.Model.extend({
        urlRoot: '/api/webentity/',
        getLikeUserCollection : function(){
            try {
                var liker_list =  this.get('limited_likers')['results'];
                return new Backbone.Collection(liker_list);
            }
            catch(e){
                return [];
            }

        },

        getLikerCount: function(){
            try{
                var liker_count = this.get('limited_likers')['count'];
                return liker_count
            }
            catch(e){
                console.warn('can not get liker count');
                return 0;
            }

        },
        parse: function(data){
            return data;
        },

    });

    return EntityModel;


});