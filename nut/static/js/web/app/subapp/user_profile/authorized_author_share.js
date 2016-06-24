define(['jquery', 'libs/Class','underscore','bootbox'], function(
    $, Class,_,bootbox
){

    var AuthorizedAuthorShare= Class.extend({
        init: function(){
            console.log('authorized author page!');
            this.share_weixin_modal_content = $('#share_weixin_modal_content').html();
            this.setupShareTrigger();
        },

        showWeixinShareDialog: function(){
            bootbox.hideAll();
            bootbox.dialog({
                title: '分享 果库授权作者 微信',
                onEscape: true,
                backdrop:true,
                closeButton: true,
                animate: true,
                className: 'media-wx-share-dialog',
                message: this.share_weixin_modal_content

            });
        },

        setupShareTrigger: function(){
            $('.authorized_author_info .user-media-wrapper .media-wechat').each(this.setupWeixinShareBtn.bind(this));
        },

        setupWeixinShareBtn: function(index, ele){
                $(ele).click(this.showWeixinShareDialog.bind(this));
        }
    });

    return AuthorizedAuthorShare;
});



