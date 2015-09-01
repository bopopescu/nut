(function(Backbone,$, _){



    var editors = Backbone.Form.editors;

    editors.Imgpicker = editors.Text.extend({
        tagName: 'div',

        events: {
            'change input[type=file]': 'sendFile',
            'click .remove': 'removeFile'
        },

        initialize: function(options) {
            _.bindAll(this, 'upload_success', 'upload_fail');
            editors.Text.prototype.initialize.call(this, options);
            this.$input = $('<input type="hidden" name="'+this.key+'" />');
            this.$uploadInput = $('<input type="file" multiple="multiple" />');
            this.$loader = $('<p class="upload-status"><span class="loader"></span> Uploading&hellip;</p>');
            this.$error = $('<p class="upload-error error">Error</p>');
            this.$image = $('<img class="table-image" src="">');
        },

        // return an array of file dicts
        getValue: function() {
            var val = this.$input.val();
            return val ;
        },

        setValue: function(value) {
            var str = value;
            this.$input.val(str);
            this.$image.attr('src',str);

        },

        render: function(options) {
            editors.Text.prototype.render.apply(this, arguments);
            this.$el.append(this.$input);
            this.$el.append(this.$uploadInput);
            this.$el.append(this.$loader.hide());
            this.$el.append(this.$error.hide());
            this.$el.append(this.$image);
            this.$image.attr('src', this.value);
            return this;
        },
        _getFileFromEvent: function(e){
            var files = e.currentTarget.files
            return files ;
        },
        sendFile:function(event){
            var  data = new FormData();
            var file = this._getFileFromEvent(event);
            data.append("file", file[0]);
            console.log('上传文件中......');
            $.ajax({
                data: data,
                type: "POST",
                //TODO:
                url: "/management/media/upload/image/?mwidth=1200;mquality=90",
                cache: false,
                contentType: false,
                processData: false,
                success: this.upload_success,
                error: this.upload_fail,
            });
        },

        upload_success: function(url){
            this.setValue(url);
            console.log(url);
        },
        upload_fail: function(data){
            console.log(data);
        },



        filepickerSuccess: function(s3Url, file) {
            console.log('File uploaded', s3Url);
            this.$loader.hide();
            this.$error.hide();
            this.$uploadInput.val('');

            var newFiles = [{
                url: s3Url,
                filename: file.name,
                size: file.size,
                content_type: file.type
            }];

            console.log('File uploaded (processed)', newFiles);
            this.setValue(this.getValue().concat(newFiles));
        },

        filepickerError: function(msg, file) {
            console.debug('Filepicker error', msg);
            this.$loader.hide();
            this.$error.show();
        },


        updateList: function(files) {
            // this code is currently duplicated as a handlebar helper (I wanted to let this
            // backbone-forms field stand on its own)
            var displayFilesize = function(bytes) {
                // TODO improve this function
                return Math.floor(bytes / 1024) + 'K';
            };

            this.$list.empty();
            _(files).each(function(file) {
                var a = $('<a>', {
                    target: '_blank',
                    href: file.url,
                    text: file.filename + ' (' + file.content_type + ') ' + displayFilesize(file.size)
                });
                var li = $('<li>').append(a);
                li.append(a, ' ', $('<a href="#" class="remove"><i class="icon-remove"></i></a>').data('url', file.url));
                this.$list.append(li);
            }, this);

            this.$list[files.length ? 'show' : 'hide']();
        },

        removeFile: function(ev) {
            if (ev) ev.preventDefault();
            var url = $(ev.currentTarget).data('url');
            var files = this.getValue();
            this.setValue(_(files).reject(function(one) {
                return one.url === url;
            }));
        }

    });

})(Backbone,jQuery,_);