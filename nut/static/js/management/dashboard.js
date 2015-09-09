/**
 *
 * Created by edison on 15/8/30.
 */

$(function(){
    var EntityModel = Backbone.Model.extend({

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
            //console.log(this.model.toJSON());
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }

    });

    var entities = new EntityList();

    var DashboardView = Backbone.View.extend({
        el: "#dashboard",

        initialize: function(){
            this.listenTo(entities, 'add', this.addOne);
            this.listenTo(entities, 'reset', this.addAll);
            this.listenTo(entities, 'all', this.render);

            this.recently = this.$("#entities-footer");
            entities.fetch();
        },

        addOne: function(entity) {
            var view = new EntityView({model: entity});
            this.$("#recently-entities ul").append(view.render().el);
        },

        addAll: function(){
            entities.each(this.addOne, this);
        },

        render : function(){
            if (entities.length) {
                this.recently.show();
            }
        }

    });

    var dashboard = new DashboardView();
});