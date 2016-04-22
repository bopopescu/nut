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
                action: 'user-follow',
                label: 'data-user-nickname',
                value: 'data-user-id',
                wrapper: '.user-page'
            },
            {
                selector: '.follow.btn-cancel',
                trigger: 'click',
                category: 'user_detail',
                action: 'user-unfollow',
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
                selector: '#user-note-panel .note-entity-img-wrapper .img-box',
                trigger: 'click',
                category: 'user-note',
                action: 'entity-detail',
                label: 'data-note-title',
                value: 'data-note-id'
            }
            //}, {
            //    selector: '#user-note-panel .note-content-wrapper .note-text',
            //    trigger: 'click',
            //    category: 'user-note',
            //    action: 'entity-detail',
            //    label: 'data-note-title',
            //    value: 'data-note-id',
            //    wrapper: '#user-note-panel'
            //}
            ,{
              selector: '#user-main-content .social-list .user-item .user-icon',
                trigger: 'click',
                category: 'user',
                action: 'user-detail',
                label: 'data-user-name',
                value: 'data-user'
            }
            ,{
              selector: '#user-main-content .social-list .user-item .user-info-wrapper .user-name a',
                trigger: 'click',
                category: 'user',
                action: 'user-detail',
                label: 'data-user-name',
                value: 'data-user'
            }
            ,{
              selector: '#user-main-content .social-list .user-item .user-info-wrapper .follow.newest-button-blue',
                trigger: 'click',
                category: 'user',
                action: 'user-follow',
                label: 'data-user-name',
                value: 'data-user-id'
            }
             ,{
              selector: '#user-main-content .social-list .user-item .user-info-wrapper .follow.new-btn-cancel',
                trigger: 'click',
                category: 'user',
                action: 'user-unfollow',
                label: 'data-user-name',
                value: 'data-user-id'
            },{
              selector: '#user-like-panel .category-list-wrapper .category-list .category-filter-item a',
                trigger: 'click',
                category: 'category',
                action: 'category-detail',
                label: 'data-category-title',
                value: 'data-category',
                wrapper: '#user-main-content'
            },{
              selector: '#user-like-panel .panel-content-wrapper .entity-cell .img-box a',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#user-main-content'
            }
            // strange bad
            //,{
            //    selector:'.panel-content-wrapper .note-cell .note-wrapper .note-entity-img-wrapper .img-box',
            //    trigger:'click',
            //    category:'note-entity',
            //    action:'entity-detail',
            //    label:'data-entity-title',
            //    value:'data-entity',
            //    wrapper:'#user-note-panel'
            //}
            ,{
              selector: '#user-article-panel .panel-content-wrapper .article-cell .article-cover',
                trigger: 'click',
                category: 'article',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#user-main-content'
            }
            ,{
              selector: '#user-article-panel .panel-content-wrapper .article-cell .article-title-link',
                trigger: 'click',
                category: 'article',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#user-main-content'
            }
            ,{
              selector: '#detail_content_right .user-following .user-icon-list li a',
                trigger: 'click',
                category: 'user',
                action: 'user-detail',
                label: 'data-user-title',
                value: 'data-user',
                wrapper: '#user-main-content'
            }
            ,{
              selector: '#detail_content_right .user-fans .user-icon-list li a',
                trigger: 'click',
                category: 'user',
                action: 'user-detail',
                label: 'data-user-title',
                value: 'data-user',
                wrapper: '#user-main-content'
            }

        ];

        var tracker = new Tracker(tracker_list);
    });
