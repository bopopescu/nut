require(
    [
    'libs/polyfills',
    'jquery',
    'subapp/page',
    'subapp/topmenu',
    'subapp/gotop',
    'subapp/selection_article_loader'
],

function (polyfill,
          jQuery,
          Page,
          Menu,
          GoTop,
          ArticleLoader
){
    var page = new Page();
    var menu = new Menu();
    var goto = new GoTop();
    var article_loader = new ArticleLoader();
    article_loader.request_url = location['pathname'];

    console.log("article list  init！");
});