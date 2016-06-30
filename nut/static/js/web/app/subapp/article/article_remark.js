define([
    'libs/Class',
    'subapp/account',
    'libs/fastdom',
    'utils/io',
    'libs/csrf',
    'underscore',
    'bootbox'
],function(
    Class,
    AccountApp,
    ArticleCommentManager,
    fastdom,
    io,
    _,
    bootbox
){
    var ArticleRemark = Class.extend({
        init: function(){
            console.log('article remark begin');
            this.accountApp = new AccountApp();
            this.firstPost = null;
            this.secondPost = null;
            this.initVisitorRemark();
            this.initUserRemarkPost();
            this.initUserReply();
        },
        checkUserLogin:function(){
            var loginData = $('#user_dash_link').attr('href');
            if(loginData){
                return true;
            }else{
                return false;
            }
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
            if(!that.checkUserLogin()){
                $('#remark-list').delegate('.remark-list-item-wrapper','click',function(){
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
        },

        initUserReply:function(){
            var that = this;
            //user login and request user is not remark user
            if(that.checkUserLogin){
                $('#remark-list').delegate('.remark-list-item-wrapper','click',function(){
                    var requestUser = $('#user_dash_link').data('user-id');
                    var replyTo = $(this).find('.remark-user').attr('user_name');
                    var remarkUserId = $(this).find('.remark-user').attr('user_id');
                    var replyToId = $(this).find('.remark-user').attr('remark_id');
                    var target = this;
                    if(requestUser != remarkUserId){
                        that.replyNotice(replyTo);
                        that.saveReplyToId(replyToId);
                    }else{
                        bootbox.confirm("确认删除评论?",function(result){
                            if(result){
                                 var $form = $('#article_remark_form');
                                 var url = $form.attr('action') + "delete/";
                                $.post(url,{deleteId:replyToId},function(res){
                                    if(res['success']){
                                        bootbox.alert('删除成功!');
                                        that.autoHideDialog();
                                        $(target).remove();
                                    }else{
                                        bootbox.alert('删除失败!请稍后尝试。');
                                    }
                                })
                            }else{
                               return ;
                            }
                        });
                    }
                });
                $('.remark-operate .remark-reply').click(function(){
                    //var requestUser = $('#user_dash_link').data('user-id');
                    var replyTo = $(this).find('.remark-user').attr('user_name');
                    //var remarkUserId = $(this).find('.remark-user').attr('user_id');
                    var replyToId = $(this).find('.remark-user').attr('remark_id');
                    var target = this;
                    that.replyNotice(replyTo);
                    that.saveReplyToId(replyToId);
                })
            }
        },
        initUserRemarkPost: function(){
            var $remark = $(".post-note");
            var $form = $remark.find("form");
            $form.on('submit', this.submitRemark.bind(this));
        },
        submitRemark: function(event){
            if(this.firstPost == null){
                this.firstPost = new Date();
            }else{
                this.secondPost = new Date();
            }
            if(this.secondPost && this.secondPost - this.firstPost < 3000){
                bootbox.alert('您的操作频繁,请稍后再尝试操作。');
                this.firstPost = this.secondPost;
                this.secondPost = null;
                event.preventDefault();
                return false;
            }
            if(this.firstPost && this.secondPost){
                this.firstPost = this.secondPost;
                this.secondPost = null;
            }
            console.log(event.currentTarget);
            var $form = $(event.currentTarget);
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
            var ajaxDatas = $ele;
            var newRemarkItem = _.template($('#new_remark_template').html());
            var datas = {
                remark_id:ajaxDatas['remark_id'],
                user:ajaxDatas['user'],
                user_id:ajaxDatas['user_id'],
                user_avatar:ajaxDatas['user_avatar'],
                user_url:ajaxDatas['user_url'],
                content:ajaxDatas['content'],
                user_reply_to:ajaxDatas['user_reply_to'],
                user_reply_to_url:ajaxDatas['user_reply_to_url'],
                create_time:ajaxDatas['create_time']
            };
            if($('#remark-list .remark-list-item-wrapper').length){
                 $(newRemarkItem(datas)).insertBefore($('#remark-list').children().first());
            }else{
                $('#remark-list').append(newRemarkItem(datas));
            }
        },
        postRemarkSuccess: function(result){
            var status = parseInt(result.status);
            if (status === 1){
                bootbox.alert('评论成功!');
                this.autoHideDialog();
                this.addNewRemark(result);
                this.cleanInput();
                this.cleanReplyNotice();
                this.cleanReplyToId();
            }else if(status === 0){
                this.postRemarkFail(result);
            }else{
                this.postRemarkFail(result);
            }
        },
        postRemarkFail: function(data){
            //should add bootbox to notice current remarking user
             bootbox.alert('评论失败!');
        },
        cleanInput:function(){
            $('#article_remark_form').find('textarea').val('');
        },
        cleanReplyNotice:function(){
            $('#article_remark_form').find('textarea').attr('placeholder','');
        },
        replyNotice:function(data){
            $('#article_remark_form').find('textarea').attr('placeholder','回复 '+data+':');
            $('#article_remark_form').find('textarea').focus();
        },
        saveReplyToId:function(data){
            $('#id_reply_to').val(data);
        },
        cleanReplyToId:function(){
            $('#id_reply_to').val('');
        },
        autoHideDialog:function(){
            window.setTimeout( function(){ bootbox.hideAll();}, 1000);
        }

    });
    return ArticleRemark;
});
