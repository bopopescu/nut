
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
            },
            {
                selector: '.follow.btn-cancel',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-unfollow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.authorized_author_info'
            },
            {
                selector: '.followings-list-link',
                trigger: 'click',
                category: 'user_detail',
                action: 'followings-list-link',
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
                selector: '.more-article-wrapper .article-cover',
                trigger: 'click',
                category: 'user_selection_article_list',
                action: 'user_article_cover',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#user-main-content'
            },
            {
                selector: '.more-article-wrapper .article-title-link',
                trigger: 'click',
                category: 'user_selection_article_list',
                action: 'user_article_like',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#user-main-content'
            }, {
                selector: '#user-main-content .content-left #user-tag-panel .panel-content-wrapper .tag-cell a',
                trigger: 'click',
                category: 'user-tag',
                action: 'user-tag-detail',
                label: 'data-tag-title',
                value: 'data-tag-id'
            }, {
                //
                selector: '#user-note-panel .note-entity-img-wrapper .img-box',
                trigger: 'click',
                category: 'user-note',
                action: 'entity-detail',
                label: 'data-note-title',
                value: 'data-note-id'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
