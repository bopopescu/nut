require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        //'subapp/yearseller/linkscroll',
        'subapp/yearseller/share',
        'subapp/yearseller/shops_slick',
        'subapp/yearseller/columns_slick',
        'subapp/discover/recommend_user_slick',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser',
        'libs/fastclick'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             //AnchorScroller,
             ShareHanlder,
             ShopsSlick,
             ColumnsSlick,
             RecommendUserSlick,
             cookie,
             TopAd,
             browser,
             FastClick

    ){

        var sellerHeader = new YearSellerHeader();
        //var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        var shopsSlick = new ShopsSlick();
        var columnsSlick = new ColumnsSlick();
        var recommendUserSlick = new RecommendUserSlick();
        //var topAd = new TopAd();
        // for weixin  access redirect entity link to  app download
        if (browser.is_weixin()){
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');
        }
        FastClick.attach(document.body);

        console.log('in year seller 2016 app');

    });
