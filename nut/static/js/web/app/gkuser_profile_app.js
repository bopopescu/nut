require([
        'jquery',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/user_follow',
        'subapp/tracker'
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
                wrapper: '.user-page'
            },
            {
                selector: '.follow.btn-cancel',
                trigger: 'click',
                category: 'user_detail',
                action: 'unfollow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            },
            {
                selector: '.user-weibo-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-weibo-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            },
            {
                selector: '.following-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'following-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            },
            {
                selector: '.fans-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'fans-list-link',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            },
            {
                selector: '.article-banner-link',
                trigger: 'click',
                category: 'authorized_author_index',
                action: 'authorized_author_index_article_banner',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '.user-article-wrapper'
            },
            {
                selector: '.article-title',
                trigger: 'click',
                category: 'authorized_author_index',
                action: 'authorized_author_index_article_title',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '.user-article-wrapper'
            },
            {
                selector: '.follow.newest-button-blue',
                trigger: 'click',
                category: 'authorized_seller_index',
                action: 'follow',
                label: 'data-shop-title',
                value: 'data-user-id',
                wrapper: '.user-page'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
