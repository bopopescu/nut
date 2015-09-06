define(function(require){

    var Article = require('models/Article').Article;
    var ArticleCollection = require('models/Article').ArticleCollection;
    var ArticleListView = require('views/article')


    var applicationController = function(){
        if(this.initialize && _.isFunction(this.initialize)){
            this.initialize.apply(this, [].slice.call(arguments));
        }
    };
    _.extend(applicationController.prototype , {
        initialize: function(){

            this.articleCollection = new ArticleCollection();
            var articleList = new ArticleListView({
                el: '#Article-management',
                collection: this.articleCollection,
            });
        }

    });
    return applicationController;

});