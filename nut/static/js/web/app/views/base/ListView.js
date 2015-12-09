define(['Backbone','libs/underscore'],
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
            _.each(collection, this.renderItem.bind(this));

        },
        renderItem: function(model){
            var itemViewClass = _.result(this,'itemView', null);
            if(_.isNull(itemViewClass)){
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