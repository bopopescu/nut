require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/linkscroll'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             AnchorScroller

    ){

        var sellerHeader = new YearSellerHeader();
        var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        console.log('in year seller app');

    });
