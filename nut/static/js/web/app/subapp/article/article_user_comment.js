define([
        'libs/Class',
        'jquery',
        'subapp/account'
    ],
    function(Class, $, AccountApp){
        var ArticleCommentManager = Class.extend({
            init: function(){
                console.log('article user comment begin.');
                this.accountApp = new AccountApp();
            }
        });
        return ArticleCommentManager;
    });
