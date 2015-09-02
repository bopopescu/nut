(function(document,window,$){

    // ployfill -----------  function.protype.bind
    if (!Function.prototype.bind) {
      Function.prototype.bind = function(oThis) {
        if (typeof this !== 'function') {
          // closest thing possible to the ECMAScript 5
          // internal IsCallable function
          throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
        }

        var aArgs   = Array.prototype.slice.call(arguments, 1),
            fToBind = this,
            fNOP    = function() {},
            fBound  = function() {
              return fToBind.apply(this instanceof fNOP
                     ? this
                     : oThis,
                     aArgs.concat(Array.prototype.slice.call(arguments)));
            };

        fNOP.prototype = this.prototype;
        fBound.prototype = new fNOP();

        return fBound;
      };
    }
    // polyfill ------------ end

    function EditorApp(){
        this.initBootbox();
        this.initSummernote();
        this.bindEvents();
        this.fix_cover_url();
        this.fillSummernote();
        this.updateEditableHeight();
        this.renderEntityCard();
        //TODO: implement a method for determin if the article is changed
        // this method should compare data in the real form , and data in the summernote, title , cover , and show-cover
    }



    EditorApp.prototype={
        renderEntityCard:function(){
            var cardList = $('.guoku-card');
            $.map(cardList, function(ele, index){
                console.log('ele : ' + ele + '  index: ' + index);
                var hash = $(ele).attr('data_entity_hash');
                if (hash){
                    var url = '/detail/' + hash + '/card/'
                    $.when($.ajax({
                        url: url,
                        method: 'GET'
                    })).then(
                        function success(data){
                            //console.log("load card success");
                            if(data.error == 0){
                                //console.log('card data ok ');
                                var newInnerHtml = $(data.html).html()
                                //console.log(newInnerHtml);
                                $(ele).html(newInnerHtml);
                                //console.log('card rendered');
                            }
                            else{
                                console.log('card data error');
                            }

                        },function fail(){
                            console.log("load card fail");
                        });
                }
            });
        },
        fix_cover_url: function(){
            // #id_cover will only save uri of the cover
            // first you should  replace #id_cover's value to  #article_full_cover's value
            // when save article , the cover value will be striped to uri again
            // #article_full_cover , will be the full url , see model's property for detail
            var full_cover_url = $('#article_full_cover').val();
            $('#id_cover').val(full_cover_url);
        },
        initSummernote: function(){
          var that = this ;
          this.contentChanged = false;
          this.error_messages = [];
          this.summer = $('.guoku_editor').summernote({
            height: 700,
            focus: true,
            onImageUpload: function(file) {
                that.sendFile(file, function(url){
                    $('.guoku_editor').summernote('insertImage', url);
                });
            },
            onChange:function(contents, $editable){
                that.contentChanged = true;
                that.updateEditableHeight();
                //console.log('changed');
            },
           });

        },

        updateEditableHeight:function(){
            $('.note-editable').css({height:'auto'});
            var editableHeight = $('.note-editable').height();
                if (!editableHeight || editableHeight < 700){
                     $('.note-editable').height(700);
                }else{
                    $('.note-editable').height(editableHeight + 40);
                }
                return editableHeight;


        },
        initBootbox:function(){
         if (!bootbox) return ;
         bootbox.setDefaults({
                 size:'small',
                 className: 'guoku-dialog',
                 closeButton: false,
                 locale: 'zh_CN',
                 className: 'guoku-dialog'
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
        get_path_from_url: function(url){
            var el = document.createElement('a');
                el.href = url;
            //remove the first slash
            return el.pathname.slice(1)

        },
        collectEditorValues: function(){
            var data = {
                title : $('.note-editor .title-input').val(),
                content: this.summer.code(),
                cover : this.get_path_from_url($('#id_cover').val()),
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
        toggleIntro: function(){
            console.log('intro');
        },

        bindEvents:function() {

            $('.fix-operate #save-draft').click(this.saveDraft.bind(this));
            $('.fix-operate #save-publish').click(this.savePublish.bind(this));
            $('.fix-operate #return-list').click(this.returnList.bind(this));
            $('.fix-operate #toggle-intro').click(this.toggleIntro.bind(this));

            $('.article-cover')
                .on('change','#cover-upload-button',this.onCoverUpload.bind(this));
            $('.note-editor')
                .on('change','input.title-input', this.onTitleChange.bind(this));

            $(window).scroll(this.onWindowScroll.bind(this));

        },

        onWindowScroll: function(){
            body_top = $('body').scrollTop();
            if (body_top>453){
                $('.note-toolbar.btn-toolbar').addClass('fixed-toolbar');
            }else{
                $('.note-toolbar.btn-toolbar').removeClass('fixed-toolbar');
            }
        },

        onTitleChange:function(event){
            this.contentChanged = true ;
        },
        _getFileFromEvent: function(e){
            var files = e.currentTarget.files
            return files ;
        },

        setCover: function(url){
            this.setBackgroundImg('.cover.article-cover', url);
            $('#id_cover').val(url);
            this.contentChanged = true;
            return ;
        },
        onCoverUpload: function(e){
            var that = this;
            var files = this._getFileFromEvent(e);
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

            if ((!data['cover']) && (data['publish'] == 2)){
                this.error_messages.push('请选择封面图');
                return false;
            }
            if ((!data['title']) || (data['title']  == '标题')){
                this.error_messages.push('请填写文章标题');
                return false;
            }

            if((!data['content']) || (data['content'] == '正文')){
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
            bootbox.alert({
                size:'small',
                message: message,

            });

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
            //bootbox.alert('保存中......');
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
            if (this.contentChanged){
                bootbox.confirm({
                message: '修改不会被保存，确认返回吗？',
                callback: function(result){
                    if(result){
                         var host = window.location.host;
                         window.location ='http://' + host+'/articles/edit/';
                    }
                    return ;
                }
                 });
            }else{
                //content not changed , just return ;
                var host = window.location.host;
                window.location ='http://' + host+'/articles/edit/';
            }

        },

        saveDraft:function(e){
            var data = this.collectEditorValues();
                data['publish'] = 1;
            this.saveArticle(data,this.saveOK.bind(this), this.saveFail.bind(this));
            e.preventDefault();
            return false;
        },

        savePublish:function(e){
            var data = this.collectEditorValues();
                data['publish'] = 2;
            this.saveArticle(data, this.publishOK.bind(this), this.saveFail.bind(this));
            e.preventDefault();
            return false;
        },

        publishOK:function(data){
            console.log(data);
            this.contentChanged = false;
            bootbox.hideAll();
            bootbox.alert( '已发布');
            window.setTimeout(function(){
                var host = window.location.host;
                var path = window.location.pathname.replace('edit/', '');
                var article_url = host + path;
                window.location = 'http://' + article_url;
                //var dash_link = $('#user_dash_link').attr('href');
                //var artilce_part = 'articles/';
                //if(dash_link){
                //  window.location = 'http://' + host + dash_link + artilce_part;
                //}

            },1000);
        },

        saveOK:function(data){
            console.log(data);
            this.contentChanged = false;
            bootbox.hideAll();
            bootbox.alert( '已保存');
            window.setTimeout(function(){
                bootbox.hideAll();
            },1000);
        },

        saveFail:function(data){
            console.log(data);
            bootbox.hideAll();
            bootbox.alert('文章保存失败，请稍后再试');
        },

        sendFile:function(file , callback){
            callback = callback || function(){};
            var  data = new FormData();
            data.append("file", file[0]);
            bootbox.alert('上传文件中......');
            $.ajax({
                data: data,
                type: "POST",
                //TODO:
                url: "/management/media/upload/image/?mwidth=1200;mquality=90",
                cache: false,
                contentType: false,
                processData: false,
                success: function(url) {
                    callback(url);
                    //bootbox.hideAll();
                    //bootbox.alert('上传成功');
                    window.setTimeout(function(){
                        bootbox.hideAll();
                    }, 1000);

                },
                error: function(data){
                    bootbox.hideAll();
                    bootbox.alert('上传失败， 请稍后再试');
                    console.log(data);
                    console.log('FILE UPLOAD FAIL');
                }
            });
        }
    };

    $(document).ready(function(){
        new EditorApp();
    })


})(document, window, jQuery)

