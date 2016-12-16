require([
        'libs/polyfills',
        'jquery',
        //'subapp/yearseller/header',
        'subapp/yearseller/yearseller_2016/index_bg_slick',
        //'subapp/yearseller/linkscroll',
        'subapp/yearseller/yearseller_2016/share_2016',
        'subapp/yearseller/shops_slick',
        'subapp/yearseller/columns_slick',
        'subapp/discover/recommend_user_slick',
        'subapp/index/category_tab_view',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser',
        'libs/fastclick'
    ],
    function(polyfill,
             $,
             //YearSellerHeader,
             IndexBgSlick,
             //AnchorScroller,
             ShareHanlder,
             ShopsSlick,
             ColumnsSlick,
             RecommendUserSlick,
             CategoryTabView,
             cookie,
             TopAd,
             browser,
             FastClick

    ){

        //var sellerHeader = new YearSellerHeader();
        var indexBgSlick = new IndexBgSlick();
        //var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        var shopsSlick = new ShopsSlick();
        var columnsSlick = new ColumnsSlick();
        var recommendUserSlick = new RecommendUserSlick();
        var category_tab_view = new CategoryTabView();
        //var topAd = new TopAd();
        // for weixin  access redirect entity link to  app download
        if (browser.is_weixin()){
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');
        }
        FastClick.attach(document.body);

    });
