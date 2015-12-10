define(['Backbone','libs/underscore'], function(
    Backbone,
    _
){

    var ItemView = Backbone.View.extend({

        render : function(){
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return ItemView;

});