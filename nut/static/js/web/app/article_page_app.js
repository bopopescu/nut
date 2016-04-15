require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker',
        'subapp/articledig',
        'subapp/articlepagecounter',
        'subapp/entitycard',
        'subapp/detailsidebar',
        'subapp/related_article_loader',
        'subapp/article/article_share',
        'subapp/user_follow',
        'libs/csrf'



    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              Tracker,
              ArticleDig,
              ArticlePageCounter,
              EntityCardRender,
              SideBarManager,
              RelatedArticleLoader,
              UserFollow,
              ArticleShareApp

    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var articleDig = new ArticleDig();
        var articlePageCounter = new ArticlePageCounter();
        var entityCardRender = new EntityCardRender();
        var sidebar = new SideBarManager();
        var relatedArticleLoader = new RelatedArticleLoader();
        var user_follow = new UserFollow();
        var shareApp = new ArticleShareApp();
        var tracker_list = [
            {
                selector : '.avatar-wrapper img',
                trigger: 'click',
                category: 'article-user',
                action: 'user-detail',
                label: 'data-user-title',
                value: 'data-user-id'
            }, {
                selector : '.writer-intro a',
                trigger: 'click',
                category: 'article-user',
                action: 'user-detail',
                label: 'data-user-title',
                value: 'data-user-id'
            }, {
                selector : '.cate-list-all li',
                trigger: 'click',
                category: 'category-tag',
                action: 'category-detail',
                label: 'data-category-title',
                value: 'data-category-id'
            }, {
                selector: '.pop-entity-wrapper',
                trigger: 'click',
                category: 'pop-entity',
                action: 'pop-entity-detail',
                label: 'data-pop-entity-title',
                value: 'data-pop-entity-id'
            }, {
                selector: '.banner-holder',
                trigger: 'click',
                category: 'banner',
                action: 'tm-detail',
                label: 'data-banner-title',
                value: 'data-banner-id'
            }, {
                selector: '.dig',
                trigger: 'click',
                category: 'article-dig',
                action: 'dig',
                label: 'data-article-title',
                value: 'data-article-id'
            }, {
                selector: '.undig',
                trigger: 'click',
                category: 'article-dig',
                action: 'undig',
                label: 'data-article-title',
                value: 'data-article-id'
            }, {
                selector: '.logo-wechat',
                trigger: 'click',
                category: 'article-share',
                action: 'wechat-share',
                label: 'data-article-title',
                value: 'data-article-id'
            }, {
                selector: '.share-btn-weibo',
                trigger: 'click',
                category: 'article-share',
                action: 'weibo-share',
                label: 'data-article-title',
                value: 'data-article-id'
            }, {
                selector: '.share-btn-qq',
                trigger: 'click',
                category: 'article-share',
                action: 'qq-share',
                label: 'data-article-title',
                value: 'data-article-id'
            }, {
                selector: '.follow.newest-button-blue',
                trigger: 'click',
                category: 'user-follow',
                action: 'follow',
                label: 'data-user-title',
                value: 'data-user-id',
                wrapper: '.article-onepage #detail_content'
            }, {
                selector: '.follow.new-btn-cancel',
                trigger: 'click',
                category: 'user-follow',
                action: 'unfollow',
                label: 'data-user-title',
                value: 'data-user-id',
                wrapper: '.article-onepage #detail_content'
            }
        ];

        var tracker = new Tracker(tracker_list);

});

