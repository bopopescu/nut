require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/index/banner',
         'subapp/discover/category_slick',
        'subapp/discover/recommend_user_slick',
        'subapp/entitylike',
        'subapp/gotop'

    ],

    function (polyfill,
              jQuery,
              Menu,
              Banner,
              CategorySlick,
              RecommendUserSlick,
              AppEntityLike,
              GoTop
              ) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var banner = new Banner();
        var category_slick = new CategorySlick();
        var recommend_user_slick = new RecommendUserSlick();
        var app_like = new  AppEntityLike();
        var goto = new GoTop();
    });
