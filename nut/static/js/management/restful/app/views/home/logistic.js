define(function(require){
    var logisticView  = $('#id-logistic-view-template').html();
    var LogisticView = Backbone.View.extend({
        className : 'grid-cell',
        initialize : function(){
            this.template = _.template(logisticView);

        },
        viewDidAppear: function(){

        },
        viewWillAppear: function(){

        },
        render : function(){
            this.el.innerHTML = this.template();
            return this;
        }

    });

    return LogisticView;

});