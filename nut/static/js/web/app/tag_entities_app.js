require(
    [
        'jquery',
        'subapp/load_tag_entity',
        'subapp/entitylike',
        'subapp/topmenu',
        'subapp/gotop',
        'subapp/tracker'
    ],
    function (
        jQuery,
        LoadTagEntity,
        AppEntityLike,
        Menu,
        GoTop,
        Tracker
    ){
        var app_load_tag_eneity = new LoadTagEntity();
        var app_like = new AppEntityLike();
        var menu = new Menu();
        var goto = new GoTop();
        var tracker_list = [
            {
                selector: '.search-entity-item .thumbnail .img-box a',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#tag-entity-list'
            },{
                selector: '.search-entity-item .thumbnail .caption .title a',
                trigger: 'click',
                category: 'entity',
                action: 'entity-detail',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#tag-entity-list'
            },{
                selector: '.search-entity-item .thumbnail .action .fa-heart-o',
                trigger: 'click',
                category: 'entity',
                action: 'like',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#tag-entity-list'
            },{
                selector: '.search-entity-item .thumbnail .action .fa-heart',
                trigger: 'click',
                category: 'entity',
                action: 'unlike',
                label: 'data-entity-title',
                value: 'data-entity',
                wrapper: '#tag-entity-list'
            }
        ];
        var tracker = new Tracker(tracker_list);

        console.log("Tag entity list init！");
});
