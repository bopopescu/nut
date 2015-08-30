define(function(require){
    "use strict";
    var BannerItemView = Backbone.View.extend({
        tagName: 'tr',
        className: 'banner-data data-holder',
        template: _.template($('#id-sbbanner-item-template').html()),
        initialize: function(){
            this.listenTo(this.model, 'sync', this.render );
        },
        events: {
          //'change input': 'changeValue',
          'click .btn-edit': 'editValue',
          'click .btn-save': 'saveValue',
        },

        editValue: function(){
            this.$('td').removeClass('value');
            this.$('.edit-save').addClass('editing');
        },
        saveValue: function(){
            this.collectData();

            var res= this.model.save({
                wait: true,
            }).then(this.success.bind(this),this.error.bind(this));
            console.log(res);
            this.$('td').addClass('value');
            this.$('.edit-save').removeClass('editing');
        },
        success: function(data){

            console.log(data);
        },

        error:function(data){
            console.log(JSON.parse(data.responseText).status[0]);
        },

        collectData: function(){
            var theView = this;
            var inputs = this.$('input[for-key]');
            inputs.each(function(index,ele){
               var  the_key  = $(ele).attr('for-key');
               var  the_value = $(ele).val();
                theView.model.set(the_key,the_value);
            });
        },

        changeValue: function(e){
            console.log('value has changed');
            console.log(e);
        },
        render: function(){
            var template = this.template;
            this.$el.html(template(this.model.toJSON()));
            return this;
        }
    });

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
                var item = new BannerItemView({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }
    });

    return BannerListView;


});