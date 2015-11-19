define(['libs/Class', 'jquery'], function(Class, $){

    var CommentManager = Class.extend({
        init: function(){
            this.setupCommentEvents();
        },
        setupCommentEvents: function(ele){
            var that = this;
            var ele = ele || document.body;
            var commentButtons = $(ele).find('.add-comment');
                commentButtons.on('click', that.doAddComment);
        },

        handleNoteEle: function($ele){
            this.setupCommentEvents($ele);
        },
        doAddComment: function(event){
            console.log(event.currentTarget);
            console.log(this);
        }
    });

    return CommentManager;

});