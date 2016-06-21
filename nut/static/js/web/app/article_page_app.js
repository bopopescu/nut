require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/articledig',
        'subapp/articlepagecounter',
        'subapp/entitycard',
        'subapp/detailsidebar',
        'subapp/related_article_loader',
        'subapp/article/article_share',
        'subapp/article/article_remark',
        'subapp/article/article_related_slick',
        'subapp/article/article_sidebar_switch',
        'subapp/user_follow',
        'libs/csrf'
    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              ArticleDig,
              ArticlePageCounter,
              EntityCardRender,
              SideBarManager,
              RelatedArticleLoader,
              ArticleRemark,
              ArticleSidebarSwitch,
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
        var articleRemark = new ArticleRemark();
        var articleSidebarSwitch = new ArticleSidebarSwitch();
        var user_follow = new UserFollow();
        var shareApp = new ArticleShareApp();

});

