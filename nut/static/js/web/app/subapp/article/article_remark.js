define([
    'libs/Class',
    'subapp/account',
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
             this.initVisitorNote();
        },
        initVisitorNote: function(){
            var that = this;
            $('#visitor_note').click(function(){
                    $.when(
                        $.ajax({
                            url: '/login/'
                        })
                    ).then(
                        function success(data){
                            var html = $(data);
                            that.accountApp.modalSignIn(html);
                        },
                        function fail(){}
                    );
            });
        }
    });
    return ArticleRemark;
});
