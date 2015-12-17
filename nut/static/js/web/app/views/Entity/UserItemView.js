define(['views/base/ItemView'], function(
    ItemView
){
    var UserItemView = ItemView.extend({
        template:'#user_cell_template',
        tagName: 'li',
    });
    return UserItemView;

});