define(function(require){
    var TestView = Backbone.View.extend({
        initialize: function(){
            console.log('in test view');
        }
    });
    return TestView;
});