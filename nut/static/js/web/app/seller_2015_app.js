require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/linkscroll',
        'subapp/yearseller/share',
        'cookie',
        'subapp/top_ad/top_ad',
        'utils/browser',
        'libs/fastclick'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             AnchorScroller,
             ShareHanlder,
             cookie,
             TopAd,
             browser,
             FastClick

    ){

        var sellerHeader = new YearSellerHeader();
        var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        var topAd = new TopAd();


        // for weixin  access redirect entity link to  app download
        if (browser.is_weixin()){
            $('a.seller-entity-link').attr('href','http://www.guoku.com/download/');
        }
        FastClick.attach(document.body);

        console.log('in year seller app');

    });
