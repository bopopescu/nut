
require([
        'libs/polyfills',
        'jquery',
        'subapp/page',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker',
        'subapp/selection_article_loader'

    ],
    function (polyfill,
              jQuery,
              Page,
              Menu,
              GoTop,
              Tracker,
              ArticleLoader

    ){
        var page = new Page();
        var menu = new Menu();
        var goto = new GoTop();
        var article_loader = new ArticleLoader();
        article_loader.request_url = location['pathname'];
        var tracker_list = [{
            selector : '.img-holder',
            trigger: 'click',
            category: 'article',
            action: 'article-detail',
            label: 'data-article-title',
            value: 'data-article-id',
            wrapper: '#selection_article_list'
         }, {
            selector : '.article-title a',
            trigger: 'click',
            category: 'article',
            action: 'article-detail',
            label: 'data-article-title',
            value: 'data-article-id',
            wrapper: '#selection_article_list'
        }
    ];
        var tracker = new Tracker(tracker_list);
        console.log("article list  init！");
});

