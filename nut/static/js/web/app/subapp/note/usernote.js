define([
    'libs/Class',
    'subapp/account',
    'subapp/tag',
    'subapp/note/notepoke',
    'subapp/note/notecomment',
    'libs/fastdom',
    'utils/io',
    'libs/csrf'


],function(
    Class,
    AccountApp,
    TagManager,
    PokeManager,
    CommentManager,
    fastdom,
    io
){
    var UserNote = Class.extend({
        init: function(){
            this.accountApp = new AccountApp();
            this.tagManager = new TagManager();
            this.pokeManager = new PokeManager();
            this.commentManager = new CommentManager();
            this.initVisitorNote();
            this.initUserNotePost();
            this.initNoteUpdateDisplay();
            this.initNoteUpdateSubmit();
            this.displayTag();
        },

        submitNote: function(event){
            console.log(event.currentTarget);
            var $form = $(event.currentTarget);
            var url = $form.attr('action');
            var $textarea = $form.find("textarea");

             if ($.trim($textarea[0].value).length === 0) {
                    $textarea[0].value = '';
                    $textarea.focus();
                }else{
                     $.when(
                         $.ajax({
                         method: 'POST',
                         url: url ,
                         data: $form.serialize()
                        })
                     ).then(
                         this.postNoteSuccess.bind(this),
                         this.postNoteFail.bind(this)
                     );
                }
            event.preventDefault();
            return false;
        },

        postNoteSuccess: function(result){
            var status = parseInt(result.status);
            if (status === 1){
                var $html = $(result.data);
                this.addNewNote($html);
                this.removePostNoteForm();
            }else if(status === 0){
                this.postNoteFail(result);
            }else{
                this.postNoteFail(result);
            }
        },
        removePostNoteForm: function(){
            $('.post-note').parent().remove();
        },
        addNewNote: function($ele){
            $ele.appendTo($(".common-note-list"));
            this.pokeManager.handleNoteEle($ele);
            this.commentManager.handleNoteEle($ele);
            this.tagManager.displayTag($ele);
            this.initNoteUpdateDisplay($ele);
            this.initNoteUpdateSubmit($ele);
        },
        getCurrentUserNoteElement: function(){
            return $('.update-note').parent().parent().parent();
        },
        initNoteUpdateSubmit: function($noteEle){
            var $noteEle = $noteEle || this.getCurrentUserNoteElement();
            if (!$noteEle || ($noteEle.length === 0)){
                return ;
            }
            var $note_update_form = $noteEle.find(".update-note-form");
            $note_update_form.on('submit',this.updateNote.bind(this));
        },

        updateNote: function(event){
            var $note_content = this.getCurrentUserNoteElement();
            var $form = $(event.currentTarget);
            var url = $form.attr('action');
            var $note_text = $form.find("textarea");
            var note_content_text = $.trim($note_text[0].value);
                note_content_text = io.clearUserInputString(note_content_text);

             if (note_content_text.length > 0) {
                 $.when(
                     $.ajax({
                        method: 'POST',
                        url : $form.attr('action'),
                        data: $form.serialize(),
                        dataType: 'json',
                     })
                 ).then(
                     this._noteUpdateSuccess.bind(this),
                     this._noteUpdateFail.bind(this)
                 );
             }

            event.preventDefault();
            return false;
        },

        _noteUpdateSuccess: function(data){
             var $noteEle = $noteEle || this.getCurrentUserNoteElement();
            var $note_content = $noteEle.find(".comment_word.content");
            var $note_update_form = $noteEle.find(".update-note-form");
             if (parseInt(data.result) === 1) {
                 $note_content.html(data.note);
                 $note_update_form.hide();
                 $note_content.show();
             }
             this.tagManager.displayTag($noteEle);
        },
        _noteUpdateFail:function(){

        },
        initNoteUpdateDisplay: function($noteEle){

            var $noteEle = $noteEle || this.getCurrentUserNoteElement();
            if (!$noteEle || ($noteEle.length === 0)){
                return ;
            }

            var $note_content = $noteEle.find(".comment_word.content");
            var $note_update_form = $noteEle.find(".update-note-form");
            var $note_text_input = $note_update_form.find('textarea');
            var origin_text = $note_content.html() || '';

            origin_text = origin_text.replace(/<(.|\n)+?>/gi, "");

            var $updateButton = $noteEle.find('.update-note');
            $updateButton.on('click', function(){
                if ($note_update_form.css('display') != 'block'){
                    $note_content.hide();
                    $note_update_form.show();
                    $note_text_input.html(origin_text);
                }else{
                    $note_update_form.hide();
                    $note_content.show();
                }
            });

            var $cancelButton = $noteEle.find('.btn-cancel');
            $cancelButton.on('click', function(){
                $note_update_form.hide();
                $note_content.show();
            });

        },

        setupUpdateNoteForm: function($ele){
            var $ele = $ele || $()
        },

        postNoteFail: function(data){
            console.log('post note fail!');
        },
        initUserNotePost: function(){
            var $note = $(".post-note");
            var $form = $note.find("form");
            var $textarea = $form.find("textarea");
            $textarea.on('focus', function(){
                $form.addClass('active');
            });
            var $cancel = $form.find('.btn-cancel');
            $cancel.on('click', function() {
           //     console.log(this);
                $form.removeClass('active');
            });

            $form.on('submit', this.submitNote.bind(this));
        },

        displayTag: function(ele){
            this.tagManager.displayTag(ele);
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