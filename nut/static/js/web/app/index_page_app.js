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
         'subapp/index/offline_shop_slick',
        'subapp/user_follow',
        //'subapp/index/hot_entity',
        'subapp/gotop',
        'subapp/tracker'

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
              OfflineShopSlick,
              UserFollow,
              //HotEntity,
              GoTop,
              Tracker
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
        var offline_shop_slick = new OfflineShopSlick();
        var user_follow = new UserFollow();
        //var hot_entity = new HotEntity();
        var goto = new GoTop();
        var tracker_list = [
            {
                selector : '.banner-image-cell',
                trigger: 'click',
                category: 'index-top-banner',
                action: 'visit',
                label: 'data-banner-value',
                value: 'data-banner',
                wrapper: '#index-banners'
            }, {
                selector: '.banner-image-cell',
                trigger: 'click',
                category: 'index-middle-banner',
                action: 'visit',
                label: 'data-banner-title',
                value: 'data-banner',
                wrapper: '#middle-page-banner'
            }
        ];
        var tracker = new Tracker(tracker_list);
    });
