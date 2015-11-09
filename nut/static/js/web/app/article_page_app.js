require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/articledig',
        'subapp/articlepagecounter',
        'subapp/entitycard'

    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              ArticleDig,
              ArticlePageCounter,
              EntityCardRender
    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var articleDig = new ArticleDig();
        var articlePageCounter = new ArticlePageCounter();
        var entityCardRender = new EntityCardRender();

        console.log("article list init!！");
});

