define(function(require){
    "use strict";
    var BannerItemView = Backbone.View.extend({
        tagName: 'li',
        className:'list-item',
        template: _.template($('#id-sbbanner-item-template').html()),

        initialize: function(){},
        render: function(){
            var template = this.template;
            this.$el.html(template(this.model.toJSON()));
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


});