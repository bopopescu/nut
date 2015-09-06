define(function(require){
    var Article = Backbone.Model.extend({
        urlRoot: "/api/articles/"
    });

    var ArticleCollection = Backbone.PageableCollection.extend({
        url: '/api/articles',
        model:Article,
        parse: function(data,options){
            Backbone.PageableCollection.prototype.parse.call(this,data, options);
            if(_.isObject(data.results)){
                return data.results;

            }else{
                return data;
            }
        },
        state:{
            pageSize: 12,
            firstPage: 1,
            currentPage: 1,
        },
        queryParams:{
            pageSize: 'page_size',
            totalRecords:'count'

        },
        parseState: function (resp, queryParams, state, options) {
                 return {totalRecords: resp.count};
        }
    });

    return {
        Article: Article,
        ArticleCollection: ArticleCollection
    }
});