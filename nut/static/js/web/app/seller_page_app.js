
require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow',
        'subapp/tracker'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             GoTop,
             UserFollow,
             Tracker

    ){
        var app_like = new  AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();
        var user_follow = new UserFollow();
         var tracker_list = [
            {
                selector: '.follow.button-blue',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-follow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.authorized_author_info'
            }, {
                selector: '.follow.btn-cancel',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-unfollow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.authorized_author_info'
            }, {
                selector: '.followings-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'followings-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            }, {
                selector: '.fans-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'fans-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            }, {
                selector: '.user-article-wrapper .user-article-item-wrapper .user-article-img',
                trigger: 'click',
                category: 'authorized_author_index',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '.user-article-wrapper'
            }, {
                selector: '.user-article-wrapper .user-article-item-wrapper .article-title',
                trigger: 'click',
                category: 'authorized_author_index',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '.user-article-wrapper'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
