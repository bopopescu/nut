require([
        'jquery',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow',
        'subapp/tracker',
    ],

    function (
        jQuery,
        Menu,
        UserFollow,
        GoTop,
        Tracker) {
        var menu = new Menu();
        var goto = new GoTop();
        var user_follow = new UserFollow();
        var tracker_list = [
            {
                selector: '.follow.button-blue',
                trigger: 'click',
                category: 'user_detail',
                action: 'follow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-info-wrapper'
            },
            {
                selector: '.follow.btn-cancel',
                trigger: 'click',
                category: 'user_detail',
                action: 'unfollow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-info-wrapper'
            },
            {
                selector: '.user-weibo-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-weibo-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-info-wrapper'
            },
            {
                selector: '.following-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'following-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-info-wrapper'
            },
            {
                selector: '.fans-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'fans-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-info-wrapper'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
