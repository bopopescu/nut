define(function(require){
    var todoTpl  = $('#id-todo-view-template').html();
    var TodoView = Backbone.View.extend({
        className : 'grid-cell',
        initialize : function(){
            this.template = _.template(todoTpl);

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

    return TodoView;

});