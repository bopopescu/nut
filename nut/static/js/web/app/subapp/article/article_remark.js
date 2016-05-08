define([
    'libs/Class',
    'subapp/account',
    'subapp/article/article_user_comment',
    'libs/fastdom',
    'utils/io',
    'libs/csrf'
],function(
    Class,
    AccountApp,
    ArticleCommentManager,
    fastdom,
    io
){
    var ArticleRemark = Class.extend({
        init: function(){
            console.log('article remark begin');
            this.accountApp = new AccountApp();
            this.articleCommentManager = new ArticleCommentManager();
        }
    });
    return ArticleRemark;
});
