define(['Backbone','libs/underscore'], function(
    Backbone,
    _
){

    var ItemView = Backbone.View.extend({

        render : function(){
            if(this.model) {
                //prepare for dirty data
                try {
                    this.$el.html(this.template(this.model.toJSON()));
                } catch(e){
                    console.log(e);
                }

            }
            return this;
        }
    });

    return ItemView;

});