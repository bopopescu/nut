define(function(require){

    var Writers = Backbone.Collection.extend({
        url: '/api/user/writers',
        parse: function(data, options){
            if(_.isObject(data.results)){
                return data.results;

            }else{
                return data;
            }
        },
    });
    return Writers;
});