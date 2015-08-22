define(function(require){
    var messageTpl  = $('#id-message-view-template').html();
    var MessageView = Backbone.View.extend({
        className : 'grid-cell',
        initialize : function(){

            this.template = _.template(messageTpl);

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

    return MessageView;

});