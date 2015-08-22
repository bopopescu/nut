define(function(require){

    var  InventoryItemView = Backbone.View.extend({

        tagName: 'li',
        className: "list-item",
        template : _.template($('#id-inventory-item-template').html()),


        initialize: function(){

        },
        render: function(){
            var template = this.template;
            this.$el.html(template(this.model.toJSON()));
            return this;
        }

    });
    var  InventoryView = Backbone.View.extend({

        events: {
            'scroll': function(e){

                console.log(e);
            }
        },
        initialize: function(){
            console.log('in inventory view');

            this.listenTo(this.collection, 'reset', this.render );
            this.listenTo(this.collection, 'add', this.collectionAdd);

            this.listContainer = this.$('.list-container');
           // this.listContainer.html('');
            this.clearEle(this.listContainer.get());

            this.collection.fetch({reset: true});

        },
        render: function(){
                this.clearEle(this.listContainer.get());
            var container = this.listContainer;

            this.collection.each(function (model) {
                if (model.get('hidden') === true) {
                    return;
                }

                var item = new InventoryItemView({
                    model: model
                });

                container.append(item.render().el);

            });
            return  this;
        }

    });
    return InventoryView;
});


