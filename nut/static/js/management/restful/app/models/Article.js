define(function(require){
    var commonTools = require('utils/common');

    var Article = Backbone.Model.extend({
        urlRoot: "/api/articles/",

        last_modified_fmt: function(){
            return commonTools.formatTime(this.get('updated_datetime'));
        },


        toJSON:function(){
            var res = Backbone.Model.prototype.toJSON.call(this);
                res.last_modified_fmt = this.last_modified_fmt();
            return res;
        },
    });

    var SelectionArticle = Backbone.Model.extend({
        urlRoot: '/api/sla/'
    });

    var SelectionArticleCollection = Backbone.PageableCollection.extend({
        url: '/api/sla/',
        model : SelectionArticle,
        parse : function(data,options){
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

    var ArticleCollection = Backbone.PageableCollection.extend({
        url: '/api/articles/?publish=2',
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
        ArticleCollection: ArticleCollection,
        SelectionArticle: SelectionArticle,
        SelectionArticleCollection: SelectionArticleCollection
    }
});