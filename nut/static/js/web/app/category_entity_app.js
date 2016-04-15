require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/load_category_entity',
        'subapp/gotop',
        'subapp/tracker'
    ],
    function (polyfill,
              jQuery,
              AppEntityLike,
              Menu,
              LoadCategoryEntity,
              GoTop,
              Tracker) {
// TODO : check if csrf work --
// TODO : make sure bind is usable
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var app_load_category_entity = new LoadCategoryEntity();
        var goto = new GoTop();
        var tracker_list = [
            {
                selector : '.img-box',
                trigger: 'click',
                category: 'category-entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '#category-entity-list'
            }, {
            //    brand title
                selector : '.title a',
                trigger: 'click',
                category: 'category-entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '#category-entity-list'
            }, {
                selector : '.fa-heart-o',
                trigger: 'click',
                category: 'category-entity',
                action: 'entity-like',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#category-entity-list'
            }, {
                selector : '.fa-heart',
                trigger: 'click',
                category: 'category-entity',
                action: 'entity-unlike',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#category-entity-list'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
