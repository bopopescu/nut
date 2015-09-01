define(function (require) {

      var   SBBanner = Backbone.Model.extend({
            urlRoot: "/api/sbbanner/"
        });

      var  SBBannerCollection = Backbone.Collection.extend({
            url:'/api/sbbanner/',
            model: SBBanner,
            parse: function(data){
                if(_.isObject(data.results)){
                    return data.results
                }else{
                    return data;
                }
            }
        });

      return {
          SBBanner: SBBanner,
          SBBannerCollection: SBBannerCollection
      }
});