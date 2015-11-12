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
        'subapp/related_article_loader'

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
              RelatedArticleLoader


    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var articleDig = new ArticleDig();
        var articlePageCounter = new ArticlePageCounter();
        var entityCardRender = new EntityCardRender();
        var sidebar = new SideBarManager();
        var relatedArticleLoader = new RelatedArticleLoader();
        console.log("article list init!！");
});

