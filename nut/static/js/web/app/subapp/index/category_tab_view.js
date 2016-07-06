
define(['jquery', 'libs/Class'], function(
    $, Class
){
    var CategoryTabView= Class.extend({
        init: function () {
            this.initHoverCategory();
            console.log('category tab view begin');
        },
        initHoverCategory:function(){
            $('.category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var dataValue = $(event.target).attr('data-value');
            console.log(dataValue);
        }
    });
    return CategoryTabView;
});



