require([
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker'
    ],
    function (
              jQuery,
              AppEntityLike,
              Menu,
              GoTop,
              Tracker) {
        var menu = new Menu();
        var app_like = new AppEntityLike();
        var goto = new GoTop();
        var tracker_list = [
            {
                selector: '.img-box',
                trigger: 'click',
                category: 'search_result',
                action: 'entity-img-link',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#selection_article_list'
            },
            {
                selector: '.title',
                trigger: 'click',
                category: 'search_result',
                action: 'entity-name-link',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#selection_article_list'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });


