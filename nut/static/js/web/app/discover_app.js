requirejs.config({
    baseUrl:base_url,
    paths: {
        libs: './libs',
        subapp: './subapp',
        jquery: 'libs/jquery-1.11.1.min',
        bootstrap: 'libs/bootstrap.min',
        fastdom: 'libs/fastdom',
        cookie: 'libs/jquery.cookie',
        utils: './utils'
    },

    shim: {
        'cookie':{
            deps:['jquery']
        },
        'bootstrap':{
            deps:['jquery']
        },
        'jquery':{
            exports:'jQuery'
        }
    }
});

require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/tracker'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             Tracker
    ){
        var menu = new Menu();
        var app_like = new  AppEntityLike();

        var tracker_list = [
            {
                selector: '.recommend-user-list li',
                trigger: 'click',
                category: 'recommend-user',
                action: 'user-detail',
                label: 'data-user-title',
                value: 'data-user-id'
            }, {
            //    category
                selector: '.category',
                trigger: 'click',
                category: 'category',
                action: 'category-detail',
                label: 'data-category-title',
                value: 'data-category-id'
            }, {
            //    img-holder
                selector: '.img-holder',
                trigger: 'click',
                category: 'hot-article',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article-id'

            }, {
                selector: '.article-title',
                trigger: 'click',
                category: 'hot-article',
                action: 'article-detail',
                label: 'data-article-title',
                value: 'data-article-id'
            },{
            //    discover_entity_list
                selector: '.search-entity-item .img-box',
                trigger: 'click',
                category: 'hot-entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '#discover_entity_list'
            }, {
                selector: '.search-entity-item .title',
                trigger: 'click',
                category: 'hot-entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '#discover_entity_list'
            }, {
                selector: '.search-entity-item .btn-like',
                trigger: 'click',
                category: 'hot-entity',
                action: 'entity-like',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#discover_entity_list'
            }, {
                 selector: '.search-entity-item .btn-unlike',
                trigger: 'click',
                category: 'hot-entity',
                action: 'entity-unlike',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#discover_entity_list'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
