define(['Backbone','underscore'],
    function(
        Backbone,
        _
    )
    {

    var listViewOptions = ['itemView']
    var ListView = Backbone.View.extend({
        initialize: function(options){
            _.extend(this, _.pick(options, listViewOptions));
        },
        render: function(){
            var collection = _.result(this, 'collection', null);
            if (_.isNull(collection)){
                throw Error('can not find collection for render');
            }
            collection.each(this.renderItem.bind(this));
        },
        renderItem: function(model){
            var itemViewClass = this.itemView;
            if(_.isUndefined(itemViewClass)){
                throw Error('can not find itemView Class');
            }
            var itemView = new itemViewClass({
                model :model
            }).render();

            this.getListContainer().append(itemView.$el)

        },
        getListContainer: function(){
            //this is a default behavior ,
            return this.$el.find('bb-list-container');
        }
    });

    return ListView;
});