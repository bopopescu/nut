define(['views/base/ItemView', 'jquery', 'underscore'], function(
    ItemView,
    $,
    _
){
    var UserItemView = ItemView.extend({
        tagName: 'li',
        className: 'user-icon-cell',
        template: _.template($('#user_cell_template').html()),
        initialize: function(){
        },
        render:function(){
            this.sizingAvatar();
            return ItemView.prototype.render.call(this);

        },
        sizingAvatar: function(){
            var user = this.model.get('user');
            var avatar = user['avatar_url'];
            if ('imgcdn.guoku.com' in avatar){
                avatar = avatar.replace('/avatar','/avatar/180');
                user['avatar_url'] = avatar;
                this.model.set('user', user);
            }
        }

    });
    return UserItemView;

});