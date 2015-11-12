define(['libs/Class','jquery'],function(Class, $){

    var AccountApp = Class.extend({
        init: function(){

        },
        modalSignIn:function(html){
            var signModal = $('#SignInModal');
            var signContent = signModal.find('.modal-content');
            if (signContent.find('.row')[0]) {
                signModal.modal('show');
            } else {
                $(html).appendTo(signContent);
                signModal.modal('show');
            }
        }
    });
    return AccountApp;
});