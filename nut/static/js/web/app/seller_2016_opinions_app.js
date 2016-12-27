require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/yearseller_2016/new_recommend_user_slick'
    ],
    function(polyfill,
             $,
             RecommendUserSlick
    ){
        var recommendUserSlick = new RecommendUserSlick();
    });