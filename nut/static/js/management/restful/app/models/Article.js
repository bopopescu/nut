define(function(require){
    var Article = Backbone.Model.extend({
        urlRoot: "/api/articles/"
    });

    var ArticleCollection = Backbone.Collection.extend({
        url: '/api/articles',
        model:Article,
        parse: function(data){
            if(_.isObject(data.results)){
                return data.results;
            }else{
                return data;
            }
        }
    });

    return {
        Article: Article,
        ArticleCollection: ArticleCollection
    }
});