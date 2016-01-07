require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/linkscroll',
        'subapp/yearseller/share',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             AnchorScroller,
             ShareHanlder,
             cookie,
             TopAd,
             browser

    ){

        var sellerHeader = new YearSellerHeader();
        var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        var topAd = new TopAd();

        // for weixin  access redirect entity link to  app download
        if (browser.is_weixin()){
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');
        }


        console.log('in year seller app');

    });
