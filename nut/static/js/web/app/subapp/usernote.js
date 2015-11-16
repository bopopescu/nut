define([
    'libs/Class',
    'subapp/account'
],function(
    Class,
    AccountApp
){
    var UserNote = Class.extend({
        init: function(){
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

    return UserNote;

});