define(['libs/Class', 'jquery', 'subapp/account'],
    function(Class, $, AccountApp){

    var CommentManager = Class.extend({
        init: function(){
            this.setupCommentEvents();
            this.accountApp = new AccountApp();
        },
        setupCommentEvents: function(ele){
            var that = this;
            var ele = ele || document.body;
            var commentButtons = $(ele).find('.add-comment');
                commentButtons.on('click', that.triggerComment.bind(this));
        },

        handleNoteEle: function($ele){
            this.setupCommentEvents($ele);
        },

        getCommentContainerByButton : function(addButton){
            return $(addButton).parent().parent().find('.note-comment-list');
        },
        triggerComment: function(event){
            var note_id = $(event.currentTarget).attr('data-note');
            var $commentContainer = this.getCommentContainerByButton(event.currentTarget);
            if ($commentContainer[0]){
                $commentContainer.slideToggle('fast');
            }else{
                var url = '/entity/note/' + note_id + '/comment/' ;
                $.when($.ajax({
                    url : url ,
                    method: 'GET'
                })).then(
                    this.loadCommentSuccess.bind(this),
                    this.loadCommentFail.bind(this)
                );
            }
        },
        loadCommentSuccess: function(data){
            var result = $.parseJSON(data);
            var note_id = result.note_id;
            var $html = $(result.data);
            this.handleCommentAction($html);

            console.log(note_id);
            var $note = $('.note-content[data-note-id="'+ note_id + '"]');
            if($note[0]){
                $html.appendTo($note);
                $html.slideToggle('fast');
            }
        },
        handleCommentAction: function($comment){
            var that = this;
            // still ugly and stinky here :(
            // todo : refactor!!!!
            var form = $comment.find('form');
            var commentText = form.find('.comment-content');
            var replyToUser = '';
            var replyToComment = '';
            $comment.find('.btn-cancel').on('click', function(){
                $comment.slideToggle('fast');
            });


            function reply(commentItem) {
           //     console.log(commentItem.find('.reply'));
                commentItem.find('.reply').on('click', function (e) {

                    var commentContent = commentItem.find('.comment-content');
                    var nickname = commentItem.find('.nickname');
                      //    console.log(nickname);
                    commentText.val('回复 ' + $.trim(nickname.text()) + ': ');
                    commentText.focus();
                    replyToUser = commentContent.attr('data-creator');
                    replyToComment = commentContent.attr('data-comment');
                      //    }
                    return false;
                });

                commentItem.find('.close').on('click', function (e) {
                    var comment_id = $(this).attr('data-comment');
                    var url = '/entity/note/comment/' + comment_id + '/delete/';
                      //    console.log(comment_id);
                    $.ajax({
                        url:url,
                        type: 'post',
                        dataType:'json',
                        success: function(data){
                      //            console.log(data);
                            if (data.status === 1) {
                                commentItem.remove();
                            }
                        }
                    });

                    return false;
                });
            }



            $comment.find('.media').each(function () {
                reply($(this));
            });



            form.on('submit', function(e) {
                var input = commentText[0];
                var text = input.value;

                text = text.replace(/^回复.*[:：]/, function (str, index) {
                    //replace start "回复" with ''
                    if (index === 0) {
                        return '';
                    }
                    return str;
                });
                text = $.trim(text);
                if (text.length > 0) {
                    var url = form[0].action;
                    var data = {
                        'content': text,
                        'reply_to_user_id': replyToUser,
                        'reply_to_comment_id': replyToComment
                    };

                    $.ajax({
                        type:"post",
                        url:url,
                        data:data,
                        success: function(result) {
                       // WTF is the following code  ?
                      //            console.log(result);
                            try {
                                result = $.parseJSON(result);
                      //                var status = parseInt(result.status);
                      //                if (status === 1) {
                                var $html = $(result.data);
                                reply($html);
                                $html.insertBefore(form);
                      //                }
                                commentText.val('');
                            } catch (err) {
                                var html = $(result);
                                that.accountApp.modalSignIn(html);
                            }
                        }
                    });
                } else {
                    input.value = '';
                    input.focus();
                }
                e.preventDefault();
                return false;
            });



        },
        loadCommentFail: function(data){
            console.log('comment load fa!il')
        }

    });

    return CommentManager;

});