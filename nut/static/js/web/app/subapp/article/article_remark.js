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
             this.initVisitorRemark();
             this.initUserRemarkPost();
             this.initUserReply();
        },
        initVisitorRemark: function(){
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
        },
        initUserReply:function(){
            var that = this;
            $('#remark-list').delegate('.remark-list-item-wrapper','click',function(){
                var replyTo = $(this).find('.remark-user').attr('user_name');
                var replyToId = $(this).find('.remark-user').attr('remark_id');
                that.replyNotice(replyTo);
                that.saveReplyToId(replyToId);
            });
        },
        initUserRemarkPost: function(){
            var $remark = $(".post-note");
            var $form = $remark.find("form");
            $form.on('submit', this.submitRemark.bind(this));
        },
        submitRemark: function(event){
            console.log(event.currentTarget);
            var $form = $(event.currentTarget);
            //var $form = $('#article_remark_form');
            var url = $form.attr('action');
            var $remarkContent = $form.find("textarea");
             if ($.trim($remarkContent[0].value).length === 0) {
                    $remarkContent[0].value = '';
                    $remarkContent.focus();
             }else{
                 $.when(
                     $.ajax({
                         cache: true,
                         type: "POST",
                         url: url ,
                         data: $form.serialize()
                     })
                 ).then(
                     this.postRemarkSuccess.bind(this),
                     this.postRemarkFail.bind(this)
                 );
                }
            event.preventDefault();
            return false;
        },
        addNewRemark: function($ele){
            $("#remark-list").append(
                '<p class="remark-list-item-wrapper">'+$ele['content']+'</p>'
            );
        },
        postRemarkSuccess: function(result){

            var status = parseInt(result.status);
            if (status === 1){
                this.addNewRemark(result);
                this.cleanInput();
                this.cleanReplyNotice();
            }else if(status === 0){
                this.postRemarkFail(result);
            }else{
                this.postRemarkFail(result);
            }
        },
        postRemarkFail: function(data){
            //should add bootbox to notice current remarking user
            console.log('post remark fail!');
        },
        cleanInput:function(){
            $('#article_remark_form').find('textarea').val('');
        },
        cleanReplyNotice:function(){
             $('#article_remark_form').find('textarea').attr('placeholder','');
        },
        replyNotice:function(data){
            $('#article_remark_form').find('textarea').attr('placeholder','回复 '+data+':');
        },
        saveReplyToId:function(data){
            $('#id_reply_to').val(data);
        }

    });
    return ArticleRemark;
});
