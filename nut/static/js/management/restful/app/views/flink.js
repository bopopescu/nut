define(function(require){
    "use strict";
    var FLinkItemForm = Backbone.Form.extend({
        initialize: function(options){
            Backbone.Form.prototype.initialize.call(this,options);
        },
        // jQuery will strip <tr><td> when create dom from str,  if  you wrap them in <form>
        tagName: 'form',
        template: _.template($('#id-flink-form-template').html()),
        schema :{
            name : {type:'Text', validators:['required',]},
            logo: {type:'Imgpicker',validators:['required'] },
            link_category: {type:'Select', options:{
                                            'OTHER': '其他',
                                            'MEDIA':'媒体网站',
                                            'DS':'设计类网站',
                                            'TECH':'科技类网站',
                                            'CHANNEL':'渠道类网站',
                                            'STARTUP':'创业类网站',
                                            }},
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


    var FLinkListView = Backbone.View.extend({
        initialize: function(){
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'add', this.collectionAdd);
            this.listenTo(this.collection, 'sync', this.sync);
            this.listContainer = this.$('.list-container');
            this.addButton = this.$('#add-flink');
            this.clearEle(this.listContainer.get());
            this.collection.fetch({reset:true});
        },

        events : {
            'click #add-flink':  'addLink'
        },

        addLink: function(){
          var newModel =   this.collection.create({
              name: '网站名称',
              link: 'http://www.guoku.com/',
              link_category: 'OTHER',
              position: 10,
              status: 1,
              logo:'www'
          });
          var itemForm = new FLinkItemForm({
              model : newModel
          });
          this.listContainer.prepend(itemForm.render().el);
        },

        sync: function(){
            console.log('collection sync');
        },

        render: function(){
            this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            this.collection.each(function(model){
                var item = new FLinkItemForm({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }
    });

    return FLinkListView;


});