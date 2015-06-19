(function(document,window){

    function EditorApp(){
        this.initSummernote();

        this.bindEvents();

        this.fillSummernote();

    }

    EditorApp.prototype={
        initSummernote: function(){
          var that = this ;
          this.error_messages = [];
          this.summer = $('.guoku_editor').summernote({
            height: 700,
            focus: true,
            onImageUpload: function(file) {
                that.sendFile(file, function(url){
                    $('.guoku_editor').summernote('insertImage', url);
                });
            }
           });

        },
        collectFormValues: function () {
           var  data = {
                cover : $('#real_article_form #id_cover').val(),
                title : $('#real_article_form #id_title').val(),
                content: $('#real_article_form #id_content').val(),
                publish: $('#real_article_form #id_publish').val(),
                showcover: $('#real_article_form #id_showcover').prop('checked')
            };

            return data;
        },

        setFormValues: function(data){
            // not used , ajax can send data directly
            $('#real_article_form #id_cover').val(data['cover']);
            $('#real_article_form #id_title').val(data['title']);
            $('#real_article_form #id_content').val(data['content']);
            $('#real_article_form #id_publish').val(data['publish']);

        },

        collectEditorValues: function(){
            var data = {
                title : $('.note-editor .title-input').val(),
                content: this.summer.code(),
                cover : $('#id_cover').val(),
                showcover : $('#showcover').prop('checked') ? 1 : 0
            };
            return data;
        },
        setEditorValues:function(data){
            $('.note-editor .title-input').val(data['title']);
            this.summer.code(data['content']);
            this.setBackgroundImg('.cover.article-cover',data['cover']);
            $('#showcover').prop('checked', data['showcover']);

        },
        getBackgroundImgUrl:function(selector){
            //not working  : ))))) ,css bgimg string to url
            return $(selector).css("backgroundImage");
        },
        setBackgroundImg:function(selector , url){
            if(url){
                $('.cover .icon-wrapper').hide();
                $(selector).css({"backgroundImage": 'url('+ url+')' });
            }
        },

        fillSummernote: function(){
            var data = this.collectFormValues();
                this.setEditorValues(data);
        },


        bindEvents:function() {

            $('.fix-operate #save-draft').click(this.saveDraft.bind(this));
            $('.fix-operate #save-publish').click(this.savePublish.bind(this));
            $('.fix-operate #return-list').click(this.returnList.bind(this));
            $('.article-cover').on('change','#cover-upload-button',this.onCoverUpload.bind(this));

        },

        getFileFromEvent: function(e){
            var files = e.currentTarget.files
            return files ;
        },

        setCover: function(url){
            this.setBackgroundImg('.cover.article-cover', url);
            $('#id_cover').val(url);
            return ;
        },
        onCoverUpload: function(e){
            var that = this;
            var files = this.getFileFromEvent(e);
            if (files){

                this.sendFile(files, this.setCover.bind(this));
            }

        },

        clearErrorMessage: function(){
            while(this.error_messages.length){
                this.error_messages.shift();
            }
            return ;
        },

        checkData: function(data){
            this.clearErrorMessage();

            if (!data['cover']){
                this.error_messages.push('请选择封面图');
                return false;
            }
            if(!data['title']){
                this.error_messages.push('请填写文章标题');
                return false;
            }

            if(!data['content']){
                this.error_messages.push('请输入文章内容');
                return false;
            }

            return true;
        },

        showErrorMessages:function(){
            var message = '';
            $.each(this.error_messages, function(idx, msg){
               message  += msg + "   ";
            });
            alert(message);

        },
        saveArticle: function(data, success,fail){
            //the article is is useless
            function k(){}
            success = success || k;
            fail = fail||k;

            if (!this.checkData(data)){
                this.showErrorMessages();
                return ;
            }
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

        returnList: function(e){
          //var data = this.collectEditorValues();
          //    data['publish'] = this.collectFormValues()['publish'];
          //this.saveArticle(data, this.saveOK, this.saveFail);
          //  e.preventDefault();
            var host = window.location.host;
            window.location ='http://' + host+'/articles/edit/';

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
            callback = callback || function(){};
            var  data = new FormData();
            data.append("file", file[0]);
            $.ajax({
                data: data,
                type: "POST",
                //TODO:
                url: "/management/media/upload/image/",
                cache: false,
                contentType: false,
                processData: false,
                success: function(url) {
                    callback(url);

                },
                error: function(data){
                    console.log(data);
                    console.log('FILE UPLOAD FAIL');
                }
            });
        }


    };

    $(document).ready(function(){
        new EditorApp();
    })


})(document, window)

