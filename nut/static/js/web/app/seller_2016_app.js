require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/yearseller_2016/index_bg_slick',
        'subapp/yearseller/yearseller_2016/share_2016',
        'subapp/yearseller/shops_slick',
        'subapp/yearseller/columns_slick',
        'subapp/yearseller/yearseller_2016/new_recommend_user_slick',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser',
        'libs/fastclick'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             IndexBgSlick,
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
        var indexBgSlick = new IndexBgSlick();
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

    });
