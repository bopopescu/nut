require([
        'libs/polyfills',
        'jquery',
        'subapp/topmenu',
        'subapp/index/banner',
        'subapp/index/middle_page_banner',

        'subapp/discover/recommend_user_slick',
        'subapp/entitylike',
        'subapp/index/entity_category_tab',
        'subapp/index/category_tab_view',
        'subapp/user_follow',
        'subapp/gotop'

    ],

    function (polyfill,
              jQuery,
              Menu,
              Banner,
              MiddlePageBanner,

              RecommendUserSlick,
              AppEntityLike,
              EntityCategoryTab,
              CategoryTabView,
              UserFollow,
              GoTop
              ) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var banner = new Banner();
        var middle_page_banner = new MiddlePageBanner();

        var recommend_user_slick = new RecommendUserSlick();
        var app_like = new  AppEntityLike();
        var entity_category_tab = new EntityCategoryTab();
        var category_tab_view = new CategoryTabView();
        var user_follow = new UserFollow();
        var goto = new GoTop();
    });
