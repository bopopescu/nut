define(function(require){
    var Article = Backbone.Model.extend({
        urlRoot: "/api/articles/"
    });

    var ArticleCollection = Backbone.PageableCollection.extend({
        url: '/api/articles/?publish=2',
        model:Article,
        //addUrlParam: function(key, value){
        //
        //},
        //getUrlParams:function(){
        //    return this.queryStringToParams(this.url);
        //},
        //
        //queryStringToParams: function (qs) {
        //    var kvp, k, v, ls, params = {}, decode = decodeURIComponent;
        //    var kvps = qs.split('&');
        //    for (var i = 0, l = kvps.length; i < l; i++) {
        //        var param = kvps[i];
        //        kvp = param.split('='), k = kvp[0], v = kvp[1] || true;
        //        k = decode(k), v = decode(v), ls = params[k];
        //        if (_isArray(ls)) ls.push(v);
        //        else if (ls) params[k] = [ls, v];
        //        else params[k] = v;
        //    }
        //    return params;
        //},
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