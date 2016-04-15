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
                selector: '.search-entity-item .img-box',
                trigger: 'click',
                category: 'search_result',
                action: 'entity-img-link',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#selection_article_list'
            },
            {
                selector: '.search-entity-item .title',
                trigger: 'click',
                category: 'search_result',
                action: 'entity-name-link',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#selection_article_list'
            }
            ,
            {
                selector: '.selection-article-item .img-link',
                trigger: 'click',
                category: 'search_result',
                action: 'article-banner',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#selection_article_list'
            }
            ,
            {
                selector: '.selection-article-item .article-title',
                trigger: 'click',
                category: 'search_result',
                action: 'article-banner',
                label: 'data-article-title',
                value: 'data-article',
                wrapper: '#selection_article_list'
            }
            ,
            {
                selector: '.search-user-item .pull-left',
                trigger: 'click',
                category: 'search_result',
                action: 'user-logo',
                label: 'data-user-name',
                value: 'data-user',
                wrapper: '#selection_article_list'
            }
            ,
            {
                selector: '.search-tag-item .search-tag-item-link',
                trigger: 'click',
                category: 'search_result',
                action: 'tag-detail',
                label: 'data-tag-name',
                value: 'data-tag',
                wrapper: '#selection_article_list'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });


