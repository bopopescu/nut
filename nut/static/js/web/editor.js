(function(document,window){

    function EditorApp(){
        this.initSummernote();

        this.bindEvents();

        this.fillSummernote();

    }

    EditorApp.prototype={
        initSummernote: function(){
          this.summer = $('.guoku_editor').summernote({
            height: 700,
            focus: true,
            onImageUpload: function(file, editor, welEditable) {
                this.sendFile(file, editor, welEditable);
            }
           });

        },
        collectFormValues: function () {
           var  data = {
                cover : $('#real_article_form #id_cover').val(),
                title : $('#real_article_form #id_title').val(),
                content: $('#real_article_form #id_content').val(),
                publish: $('#real_article_form #id_publish').val(),
            };

            return data;
        },

        setFormValues: function(data){
            $('#real_article_form #id_cover').val(data['cover']);
            $('#real_article_form #id_title').val(data['title']);
            $('#real_article_form #id_content').val(data['content']);
            $('#real_article_form #id_publish').val(data['publish']);

        },

        collectEditorValues: function(){
            var data = {
                title : $('.note-editor .title-input').val(),
                content: this.summer.code(),
                cover : this.getBackgroundImgUrl('.article-cover')
            };
            return data;
        },
        setEditorValues:function(data){
            $('.note-editor .title-input').val(data['title']);
            this.summer.code(data['content']);
            this.setBackgroundImg('.article-cover',data.cover);
        },
        getBackgroundImgUrl:function(selector){
            return $(selector).css("backgroundImage");
        },
        setBackgroundImg:function(selector , url){
            $(selector).css({"backgroundImage":url});
        },
        fillSummernote: function(){
            var data = this.collectFormValues();
                this.setEditorValues(data);
        },

        bindEvents:function(){
            $('.fix-operate #save-draft').click(this.saveDraft.bind(this));
            $('.fix-operate #save-publish').click(this.savePublish.bind(this));

        },


        saveArticle: function(data, success,fail){
            //the article is is useless
            function k(){}
            success = success || k;
            fail = fail||k;

            var that = this;
            var url = window.location.pathname;
                $.when(
                    $.ajax({
                        url: url,
                        data: data,
                        method: 'POST'
                    })
                ).then(
                    success,
                    fail
                )
        },

        saveDraft:function(e){
            var data = this.collectEditorValues();
                data['publish'] = 1;
            this.saveArticle(data,this.saveOK, this.saveFail);
            e.preventDefault();
            return false;
        },

        savePublish:function(e){
            var data = this.collectEditorValues();
                data['publish'] = 2;
            this.saveArticle(data, this.saveOK, this.saveFail);
            e.preventDefault();
            return false;
        },

        saveOK:function(){
            alert('save ok!');
        },
        saveFail:function(){
            alert('save fail');
        },

        sendFile:function(file , callback){
            var  data = new FormData();
            data.append("file", file[0]);
            $.ajax({
                data: data,
                type: "POST",
                url: "{% url 'management_upload_image' %}",
                cache: false,
                contentType: false,
                processData: false,
                success: function(url) {
                    //handel
                   callback(url);

                },
                error: function(){

                }
            });
        }


    };

    $(document).ready(function(){
        new EditorApp();
    })


})(document, window)

