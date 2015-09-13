define(function (require) {

      var   FLink = Backbone.Model.extend({
            urlRoot: "/api/flink/"
        });

      var  FLinkCollection = Backbone.Collection.extend({
            url:'/api/flink/',
            model: FLink,
            parse: function(data){
                if(_.isObject(data.results)){
                    return data.results
                }else{
                    return data;
                }
            }
        });

      return {
          FLink: FLink,
          FLinkCollection: FLinkCollection
      }
});