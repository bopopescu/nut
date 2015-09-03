define(function(require){
    "use strict";

    var ArticleListItemView = Backbone.View.extend({
        initialize: function(){
            Backbone.View.prototype.initialize.apply(this,[].slice.call(arguments));
        },
        tagName: 'tr',
        template : _.template($('#id_article_list_item_template').html()),
        events : {},
        render: function(){
            this.$el.html(this.template(this.model.toJSON()))
            return this ;
        }

    });

    var ArticleListView = Backbone.View.extend({
        initialize: function(){
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'sync', this.sync);
            this.listContainer = this.$('.list-container');
            this.clearEle(this.listContainer.get());
            this.collection.fetch({reset:true});
        },
        render: function(){
            this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            this.collection.each(function(model){
                var item = new ArticleListItemView({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }

    });

    return ArticleListView ;



});