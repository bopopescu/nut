define(function(require){
    "use strict";
    var BannerItemForm = Backbone.Form.extend({
        initialize: function(options){
            Backbone.Form.prototype.initialize.call(this,options);
        },
        tagName: 'form',
        template: _.template($('#id-sbbanner-form-template').html()),
        schema :{
            image: {type:'Imgpicker'},
            position: 'Number',
            link:'Text',
            status: {type:'Select', options:{0: '移除', 1:'不激活',2:'激活'}}
        },
        events:{
            'click .btn-edit': 'editValue',
            'click .btn-save': 'saveValue',
            'change': 'showSaveButton'
        },
        editValue: function(){
            console.log(this);
        },
        saveValue: function(){
            console.log(this);
            this.commit();
            this.model.save();
            this.hideSaveButton();
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
            this.listContainer = this.$('.list-container');
            this.clearEle(this.listContainer.get());
            this.collection.fetch({reset:true});
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