define(['libs/Class', 'jquery', 'underscore','bootbox'], function(Class,$,_,bootbox){

    var ShareHanlder = Class.extend({
        init: function(){

            this.share_weixin_modal_content = $('#share_friends_modal_content').html();

            this.weixinShareOptions ={

            };

            //what
            this.setupShareTrigger();

        },

        showWeixinShareDialog: function(){
            bootbox.hideAll();
            bootbox.dialog({
                title: '分享 share with friends',
                onEscape: true,
                backdrop:true,
                closeButton: true,
                animate: true,
                className: 'share-friends-dialog',
                message: this.share_weixin_modal_content,

            });
        },

        setupShareTrigger: function(){

            $('#share').setupWeixinShareSellerBtn.bind(this);
        },

        setupWeixinShareSellerBtn: function(index, ele){
                $(ele).click(this.showWeixinShareDialog.bind(this));
        },
    });
    return ShareHanlder
});
