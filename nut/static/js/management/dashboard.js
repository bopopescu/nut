/**
 *
 * Created by edison on 15/8/30.
 */

$(function(){
    var EntityModel = Backbone.Model.extend({

        parse : function(data){
            console.log(data);
        }
    });

    var EntityList = Backbone.Collection.extend({
        url: '/api/entities/',
        models: EntityModel,

        parse: function(data){
            return data.results;
        },

        done: function() {
            return this.where({done: true});
        }


    });

    var EntityView = Backbone.View.extend({
        tagName: "li",
        className: "item",
        template: _.template($("#entity-template").html()),

        initialize: function(){
            this.listenTo(this.model, 'change', this.render);
        },

        render: function(){
            console.log(this.model.toJSON());
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }

    });

    var entities = new EntityList();

    var EntityListView = Backbone.View.extend({
        el: "#recently-entities",

        initialize: function(){
            this.listenTo(entities, 'add', this.addOne);

            entities.fetch();
        },

        addOne: function(entity) {
            var view = new EntityView({model: entity});
            this.$("ul").append(view.render().el);
        }

    });

    var entitiesView = new EntityListView();
});