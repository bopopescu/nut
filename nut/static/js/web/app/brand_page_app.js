
require([
        'libs/polyfills',
        'jquery',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker'
    ],
    function(polyfill,
             jQuery,
             AppEntityLike,
             Menu,
             GoTop,
             Tracker
    ){
        var app_like = new  AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();
        var tracker_list = [
            {
            //    brand-basic-info
                selector: '.brand-basic-info a',
                trigger: 'click',
                category: 'brand',
                action: 'brand-website',
                label: 'data-brand-title',
                value: 'data-brand-id',

            }, {
                selector: '.img-box',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',

            }, {
                //    img-box
                selector: '.img-box',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '.entity-wrapper'
            },{
                selector: '.title a',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity-id',
                wrapper: '.entity-wrapper'

            }, {
                selector : '.fa-heart-o',
                trigger: 'click',
                category: 'entity',
                action: 'like',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '.entity-wrapper'
            }, {
                selector: '.fa-heart',
                trigger: 'click',
                category: 'entity',
                action: 'unlike',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '.entity-wrapper'
            }
        ];

        var tracker = new Tracker(tracker_list);
    });
