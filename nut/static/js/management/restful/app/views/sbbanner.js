define(function(require){
    "use strict";
    var BannerItemForm = Backbone.Form.extend({
        initialize: function(options){
            Backbone.Form.prototype.initialize.call(this,options);
        },
        // jQuery will strip <tr><td> when create dom from str,  if  you wrap them in <form>
        tagName: 'form',
        template: _.template($('#id-sbbanner-form-template').html()),
        schema :{
            image: {type:'Imgpicker',validators:['required'] },
            position: {type:'Number', validators: ['required','number']},
            link:{type:'Text', validators:['required','url']},
            status: {type:'Select', options:{0: '移除', 1:'不激活',2:'激活'}}
        },
        events:{
            'click .btn-edit': 'editValue',
            'click .btn-save': 'saveValue',
            'change': 'showSaveButton',
            'click .btn-delete': 'deleteEntry'
        },

        deleteEntry: function(){
            if (window.confirm('确认要删除吗？')){
                 this.model.destroy();
                    this.$el.remove();
            }


        },
        editValue: function(){
            console.log(this);
        },
        saveValue: function(){
            console.log(this);
            var error_obj = this.commit();


            if (_.isUndefined(error_obj)){
                 this.model.save();
                 this.hideSaveButton();
            }else{
                var msg = 'error: \n';
                _.map(error_obj, function(value, key){
                   console.log( key + ' : ' + value.message );
                   msg = msg + key + ' :  ' +  value.message + '\n';
                });
                alert(msg);
            }

        },
        showSaveButton:function(){
            console.log('changed! show button');
            this.getSaveButton().show();
        },
        hideSaveButton:function(){
            console.log("hide button !")
            this.getSaveButton().hide();
        },
        getSaveButton:function(){
            this._saveButton = this._saveButton || this.$('.edit-save .btn-save');
            return this._saveButton;
        },
        render: function(){
            Backbone.Form.prototype.render.call(this);
            this.getSaveButton().hide();
            return this;
        }
    });

    //var BannerItemView = Backbone.View.extend({
    //    tagName: 'tr',
    //    className: 'banner-data data-holder',
    //    template: _.template($('#id-sbbanner-item-template').html()),
    //    initialize: function(){
    //        this.listenTo(this.model, 'sync', this.render );
    //    },
    //    events: {
    //      //'change input': 'changeValue',
    //      'click .btn-edit': 'editValue',
    //      'click .btn-save': 'saveValue',
    //    },
    //
    //    editValue: function(){
    //        this.$('td').removeClass('value');
    //        this.$('.edit-save').addClass('editing');
    //    },
    //    saveValue: function(){
    //        this.collectData();
    //
    //        var res= this.model.save({
    //            wait: true,
    //        }).then(this.success.bind(this),this.error.bind(this));
    //        console.log(res);
    //        this.$('td').addClass('value');
    //        this.$('.edit-save').removeClass('editing');
    //    },
    //    success: function(data){
    //
    //        console.log(data);
    //    },
    //
    //    error:function(data){
    //        console.log(JSON.parse(data.responseText).status[0]);
    //    },
    //
    //    collectData: function(){
    //        var theView = this;
    //        var inputs = this.$('input[for-key]');
    //        inputs.each(function(index,ele){
    //           var  the_key  = $(ele).attr('for-key');
    //           var  the_value = $(ele).val();
    //            theView.model.set(the_key,the_value);
    //        });
    //    },
    //
    //    changeValue: function(e){
    //        console.log('value has changed');
    //        console.log(e);
    //    },
    //    render: function(){
    //        var template = this.template;
    //        this.$el.html(template(this.model.toJSON()));
    //        return this;
    //    }
    //});

    var BannerListView = Backbone.View.extend({
        initialize: function(){
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'add', this.collectionAdd);
            this.listenTo(this.collection, 'sync', this.sync);
            this.listContainer = this.$('.list-container');
            this.addButton = this.$('#add-sbbanner');
            this.clearEle(this.listContainer.get());
            this.collection.fetch({reset:true});
        },

        events : {
            'click #add-sbbanner':  'addBanner'
        },

        addBanner: function(){
          var newModel =   this.collection.create({
              image: 'WWW',
              position: 10,
              link: 'http://www.guoku.com/',
              status:1
          });
          var newBannerItemForm = new BannerItemForm({
              model : newModel
          });
          this.listContainer.prepend(newBannerItemForm.render().el);
        },

        sync: function(){
            console.log('collection sync');
        },

        render: function(){
            this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            this.collection.each(function(model){
                var item = new BannerItemForm({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }
    });

    return BannerListView;


});