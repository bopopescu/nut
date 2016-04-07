require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker',
        'subapp/scrollview_selection',
        'masonry',
        'jquery_bridget',
        'images_loaded'
    ],

    function (polyfill,
              jQuery,
              AppEntityLike,
              Menu,
              GoTop,
              Tracker,
              ScrollEntity

    ) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var app_scrollentity = new ScrollEntity();
        var goto = new GoTop();
        var tracker_list = [
            {
                selector : 'btn-like',
                event: 'click',
                category: 'entity',
                action: 'like',
                label: 'data-entity-title',
                value: 'data-entity'
            }, {
                selector: 'btn-unlike',
                event: 'click',
                category: 'entity',
                action: 'unlike',
                label: 'data-entity-title',
                value: 'data-entity'
            }, {
                selector: 'entity_img_link',
                event: 'click',
                category: 'entity',
                action: 'like',
                label: 'data-entity-title',
                value: 'data-entity'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
