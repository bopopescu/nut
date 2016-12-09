require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/share',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser',
        'libs/fastclick'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             ShareHanlder,
             cookie,
             TopAd,
             browser,
             FastClick

    ){
        var sellerHeader = new YearSellerHeader();
        var shareHandler = new ShareHanlder();
        //var topAd = new TopAd();
        // for weixin  access redirect entity link to  app download
        if (browser.is_weixin()){
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');
        }
        FastClick.attach(document.body);

        console.log('in year seller 2016 shops app.');

    });
