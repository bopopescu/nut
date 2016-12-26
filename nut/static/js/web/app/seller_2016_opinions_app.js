require([
        'libs/polyfills',
        'jquery',
        'subapp/discover/recommend_user_slick'
    ],
    function(polyfill,
             $,
             RecommendUserSlick
    ){
        var recommendUserSlick = new RecommendUserSlick();
    });