require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/index/banner',
        'subapp/index/middle_page_banner',

        'subapp/discover/category_slick',
        'subapp/discover/recommend_user_slick',
        'subapp/entitylike',
        'subapp/index/entity_category_tab',
        'subapp/index/category_tab_view',
        'subapp/gotop'

    ],

    function (polyfill,
              jQuery,
              Menu,
              Banner,
              MiddlePageBanner,

              CategorySlick,
              RecommendUserSlick,
              AppEntityLike,
              EntityCategoryTab,
              CategoryTabView,
              GoTop
              ) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var banner = new Banner();
        var middle_page_banner = new MiddlePageBanner();

        var category_slick = new CategorySlick();
        var recommend_user_slick = new RecommendUserSlick();
        var app_like = new  AppEntityLike();
        var entity_category_tab = new EntityCategoryTab();
        var category_tab_view = new CategoryTabView();
        var goto = new GoTop();
    });
