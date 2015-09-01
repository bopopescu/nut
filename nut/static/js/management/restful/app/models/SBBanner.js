define(function (require) {

      var   SBBanner = Backbone.Model.extend({
            urlRoot: "/management/restful/sbbanners/"
        });

      var  SBBannerCollection = Backbone.Collection.extend({
            url:'/management/restful/sbbanners/',
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